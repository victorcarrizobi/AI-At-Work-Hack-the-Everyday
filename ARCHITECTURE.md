# Architecture -- Supply Chain Risk Monitor

## System Overview

A real-time supplier risk scoring and alerting pipeline built entirely on Snowflake, using Dynamic Tables for continuous refresh, Cortex AI functions for intelligent classification and sentiment analysis, and Streamlit-in-Snowflake for visualization.

```
                         AUTO_MFG_DW (Challenge Dataset)
                    ┌─────────────┬──────────────┬──────────────┐
                    │  SUPPLIERS  │   DEFECTS    │  WARRANTY    │
                    │  (400 rows) │ (8,000 rows) │  CLAIMS      │
                    │             │              │ (30,000 rows)│
                    └──────┬──────┴──────┬───────┴──────┬───────┘
                           │             │              │
                           │    AI_CLASSIFY             │  SENTIMENT
                           │    (defect text            │  (complaint
                           │     -> risk category)      │   verbatim -> score)
                           │             │              │
                    ┌──────▼─────────────▼──────────────▼───────┐
                    │    SUPPLIER_QUALITY_SCORE (Dynamic Table)  │
                    │    400 rows | TARGET_LAG = 1 hour          │
                    │    Composite Risk Score per supplier       │
                    └──────────────────┬────────────────────────┘
                           │           │            │
                    ┌──────▼──────┐    │     ┌──────▼──────────────┐
                    │ AT_RISK_    │    │     │ SUPPLIER_RISK_ALERT │
                    │ PURCHASE_   │    │     │ (Alert, 60-min)     │
                    │ ORDERS (DT) │    │     │ -> ALERT_HISTORY    │
                    │ 14,434 rows │    │     └─────────────────────┘
                    └─────────────┘    │
                                       │     ┌──────────────────────┐
                                       ├────>│ RISK_SCORE_SNAPSHOT  │
                                       │     │ (Task, daily 6 AM)   │
                                       │     │ -> RISK_SCORE_HISTORY│
                                       │     └──────────────────────┘
                                       │
                                       │     ┌──────────────────────┐
                                       └────>│ UNMANAGED_RISK_COUNT │
                                             │ (DMF)                │
                                             └──────────────────────┘
                                       │
                    ┌──────────────────▼───────────────────────────┐
                    │          SUPPLY_CHAIN_MONITOR                │
                    │          (Streamlit-in-Snowflake)            │
                    │  5 tabs | AI_COMPLETE on-demand summaries    │
                    └─────────────────────────────────────────────┘
```

---

## Data Sources

All source data comes from `AUTO_MFG_DW`, a challenge dataset provided for the hackathon simulating an automotive manufacturing data warehouse.

| Schema.Table | Rows | Role in Pipeline |
|---|---|---|
| SUPPLY_CHAIN.SUPPLIERS | 400 | Supplier master: name, tier, country, quality rating, on-time delivery % |
| QUALITY.DEFECTS | 8,000 | Defect records with free-text descriptions -- input to AI_CLASSIFY |
| QUALITY.WARRANTY_CLAIMS | 30,000 | Customer complaint verbatim text -- input to SENTIMENT |
| SUPPLY_CHAIN.PURCHASE_ORDERS | ~50,000 | PO records with status, quantities, prices, dates |
| PRODUCTION.PARTS_CATALOG | 5,000 | Part metadata (category, name) |
| QUALITY.INSPECTIONS | 25,000 | Inspection records (not directly used in scoring) |

---

## Object Inventory

All pipeline objects live in `DEFAULT_DATABASE.PUBLIC`:

| Object | Type | Refresh | Purpose |
|---|---|---|---|
| SUPPLIER_QUALITY_SCORE | Dynamic Table | 1-hour TARGET_LAG (full refresh) | Core scoring engine -- aggregates risk per supplier |
| AT_RISK_PURCHASE_ORDERS | Dynamic Table | 1-hour TARGET_LAG | Joins open POs against supplier risk scores |
| SUPPLIER_RISK_ALERT | Alert | Every 60 minutes | Fires when CRITICAL suppliers are not SUSPENDED/PROBATION |
| RISK_SCORE_SNAPSHOT | Task | Daily at 6 AM ET | Snapshots all risk scores for trend tracking |
| ALERT_HISTORY | Table | Written by Alert | Audit log of alert firings |
| RISK_SCORE_HISTORY | Table | Written by Task | Historical risk score snapshots |
| UNMANAGED_RISK_COUNT | Data Metric Function | Manual | Counts at-risk suppliers not yet actioned |
| STREAMLIT_STAGE | Stage | N/A | Hosts streamlit_app.py |
| SUPPLY_CHAIN_MONITOR | Streamlit App | N/A | Frontend dashboard |

---

## Composite Risk Score Formula

Each supplier receives a score from 0 to 100 (higher = worse):

```
COMPOSITE_RISK_SCORE =
    0.30 x AI_RISK_SCORE           -- AI-classified defect severity
  + 0.20 x DEFECT_VOLUME_SCORE     -- Normalized defect count
  + 0.20 x INVERSE_QUALITY_SCORE   -- 100 minus baseline quality rating
  + 0.15 x WARRANTY_VOLUME_SCORE   -- Normalized warranty claim count
  + 0.15 x NEGATIVE_SENTIMENT      -- Normalized negative sentiment
```

### Component Details

__AI_RISK_SCORE__ (30% weight):
Each of 8,000 defect descriptions is classified by `SNOWFLAKE.CORTEX.AI_CLASSIFY` into one of four categories, each mapped to a numeric severity:

| Category | Severity Score |
|---|---|
| SAFETY_CRITICAL | 100 |
| PERFORMANCE | 70 |
| COSMETIC | 30 |
| WEAR_AND_TEAR | 15 |

The AI_RISK_SCORE for a supplier is the average severity across all their defects.

__DEFECT_VOLUME_SCORE__ (20% weight):
`MIN(total_defects / max_defects_across_all_suppliers * 100, 100)`

__INVERSE_QUALITY_SCORE__ (20% weight):
`100 - BASELINE_QUALITY_RATING` from the supplier master record.

__WARRANTY_VOLUME_SCORE__ (15% weight):
`MIN(warranty_claims / max_claims_across_all_suppliers * 100, 100)`

__NEGATIVE_SENTIMENT__ (15% weight):
`MIN(ABS(MIN(avg_sentiment, 0)) * 100, 100)` -- only negative sentiment contributes.

### Risk Thresholds

| Score Range | Level | Action Expected |
|---|---|---|
| >= 58 | CRITICAL | Immediate review, consider SUSPENSION |
| 38 - 57 | WARNING | Monitor closely, plan mitigation |
| < 38 | HEALTHY | Normal operations |

---

## Dynamic Table Chain

The two Dynamic Tables form a chain: DT2 reads DT1.

__DT1: SUPPLIER_QUALITY_SCORE__
- Reads from: AUTO_MFG_DW.SUPPLY_CHAIN.SUPPLIERS, QUALITY.DEFECTS, QUALITY.WARRANTY_CLAIMS, SUPPLY_CHAIN.PURCHASE_ORDERS
- Calls: AI_CLASSIFY (8,000 defect descriptions), SENTIMENT (30,000 warranty verbatims)
- Uses CURRENT_TIMESTAMP() -- forces FULL refresh mode
- Output: 400 rows, one per supplier

__DT2: AT_RISK_PURCHASE_ORDERS__
- Reads from: AUTO_MFG_DW.SUPPLY_CHAIN.PURCHASE_ORDERS, PRODUCTION.PARTS_CATALOG, and DT1 (SUPPLIER_QUALITY_SCORE)
- Filters: Only open POs (PENDING, CONFIRMED, SHIPPED) where supplier risk is WARNING or CRITICAL
- Calculates: DOLLAR_EXPOSURE = QUANTITY_ORDERED x UNIT_PRICE
- Output: ~14,434 rows

Both use TARGET_LAG = '1 hour'. When source data changes, DT1 refreshes first, then DT2 picks up the new scores.

---

## Cortex AI Functions

### AI_CLASSIFY (in DT1)

```sql
SNOWFLAKE.CORTEX.AI_CLASSIFY(
    d.DEFECT_DESCRIPTION,
    ['SAFETY_CRITICAL', 'PERFORMANCE', 'COSMETIC', 'WEAR_AND_TEAR']
)
```

Classifies each defect's free-text description into a risk category. Applied to all 8,000 defect records during each DT refresh.

### SENTIMENT (in DT1)

```sql
SNOWFLAKE.CORTEX.SENTIMENT(wc.CUSTOMER_VERBATIM)
```

Scores each warranty claim's customer complaint text on a scale of -1 (very negative) to +1 (very positive). Applied to all 30,000 warranty claims during each DT refresh.

### AI_COMPLETE (in Streamlit, on-demand)

```sql
SNOWFLAKE.CORTEX.AI_COMPLETE('llama3.1-8b', prompt)
```

Generates a 2-3 sentence natural-language risk summary for a selected supplier, including a recommended action. Called only when the user clicks "Generate AI Risk Summary" on the Supplier Deep Dive tab.

---

## Alert and Task

### SUPPLIER_RISK_ALERT

- __Schedule:__ Every 60 minutes
- __Condition:__ Fires when any supplier has RISK_LEVEL = 'CRITICAL' and CURRENT_STATUS not in ('SUSPENDED', 'PROBATION')
- __Action:__ Inserts a row into ALERT_HISTORY with: timestamp, critical supplier count, total at-risk exposure, top risk supplier name and score, and a human-readable message

### RISK_SCORE_SNAPSHOT

- __Schedule:__ Daily at 6:00 AM Eastern (CRON `0 6 * * * America/Detroit`)
- __Action:__ Copies all 400 rows from SUPPLIER_QUALITY_SCORE into RISK_SCORE_HISTORY with a snapshot timestamp
- __Purpose:__ Enables trend analysis (score changes over days/weeks)

---

## Grants Required

Dynamic Tables, Tasks, and Alerts run under the owner role (ATTENDEE_ROLE) without secondary roles. These grants were applied:

```sql
GRANT USAGE ON DATABASE AUTO_MFG_DW TO ROLE ATTENDEE_ROLE;
GRANT USAGE ON ALL SCHEMAS IN DATABASE AUTO_MFG_DW TO ROLE ATTENDEE_ROLE;
GRANT SELECT ON ALL TABLES IN DATABASE AUTO_MFG_DW TO ROLE ATTENDEE_ROLE;
GRANT EXECUTE DATA METRIC FUNCTION ON ACCOUNT TO ROLE ATTENDEE_ROLE;
```

See GOTCHA.md (GOTCHA-001) for the full story.

---

## Known Limitations

1. __Full refresh mode:__ CURRENT_TIMESTAMP() in DT1 forces full refresh. Every hour, AI_CLASSIFY runs on 8,000 rows and SENTIMENT on 30,000 rows. Production fix: move the timestamp to a downstream view.
2. __DMF auto-attach fails:__ The UNMANAGED_RISK_COUNT DMF exists and works manually but cannot be attached to the DT via ALTER TABLE. Suspected trial account limitation. Logic is embedded in the Streamlit app instead.
3. __Single model available:__ Only `llama3.1-8b` works for AI_COMPLETE on this account. Other models return deprecated or unknown errors.
4. __No incremental refresh for DT2:__ Because DT2 depends on DT1 (which is full-refresh), DT2 also effectively rebuilds each cycle.

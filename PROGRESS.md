# Supply Chain Monitor -- Progress Tracker

## Project Overview

- **Event:** Data in the D 2026 Hackathon
- **Track:** Hack the Grind
- **Project:** Supply Chain Risk Monitor
- **Database:** AUTO_MFG_DW (challenge dataset)
- **Target Schema:** DEFAULT_DATABASE.PUBLIC
- **Streamlit App:** SUPPLY_CHAIN_MONITOR

---

## Steps Completed

### Step 1: Dynamic Table -- SUPPLIER_QUALITY_SCORE
- **Status:** DONE
- **Session:** CoCo Session 1 (2026-10-16)
- **What:** Created a Dynamic Table (TARGET_LAG 1 hour) that aggregates per-supplier risk metrics from defects, warranty claims, and purchase orders.
- **AI Used:**
  - `AI_CLASSIFY` on 8,000 defect descriptions to categorize risk (SAFETY_CRITICAL, PERFORMANCE, COSMETIC, WEAR_AND_TEAR)
  - `SENTIMENT` on 30,000 warranty customer verbatim text to gauge complaint severity
- **Output:** 400 suppliers scored with composite risk (0-100). 20 CRITICAL, 268 WARNING, 112 HEALTHY.
- **Key Columns:** COMPOSITE_RISK_SCORE, RISK_LEVEL, AI_RISK_SCORE, SAFETY_CRITICAL_DEFECTS, AVG_CUSTOMER_SENTIMENT

### Step 2: Dynamic Table -- AT_RISK_PURCHASE_ORDERS
- **Status:** DONE
- **Session:** CoCo Session 1 (2026-10-16)
- **What:** Joins open POs (PENDING, CONFIRMED, SHIPPED) against SUPPLIER_QUALITY_SCORE. Flags POs where supplier risk is CRITICAL or WARNING.
- **Output:** 14,434 at-risk POs with $182.8B total dollar exposure (1,026 from CRITICAL suppliers).
- **Includes:** Part name/category, shipping mode, destination plant, dollar exposure per PO.

### Step 3: Data Metric Function -- UNMANAGED_RISK_COUNT
- **Status:** DONE (partial)
- **Session:** CoCo Session 1 (2026-10-16)
- **What:** Custom DMF that counts suppliers scored CRITICAL/WARNING but not yet SUSPENDED or on PROBATION.
- **Limitation:** DMF was created successfully and is callable manually, but auto-attaching to the Dynamic Table via ALTER TABLE ADD DATA METRIC FUNCTION failed (see GOTCHA.md). The equivalent logic is embedded directly in the Streamlit dashboard.

### Step 4: Alert -- SUPPLIER_RISK_ALERT
- **Status:** DONE
- **Session:** CoCo Session 1 (2026-10-16)
- **What:** Snowflake Alert on a 60-minute schedule. Fires when CRITICAL-risk suppliers exist with non-SUSPENDED status. Logs to ALERT_HISTORY table with critical supplier count, total at-risk exposure, top risk supplier name/score, and a message.
- **State:** RESUMED (active)

### Step 5: Task -- RISK_SCORE_SNAPSHOT
- **Status:** DONE
- **Session:** CoCo Session 1 (2026-10-16)
- **What:** Scheduled Task (CRON 0 6 * * * America/Detroit) that snapshots all supplier risk scores into RISK_SCORE_HISTORY for trend tracking.
- **State:** RESUMED (active)
- **Tables Created:** ALERT_HISTORY, RISK_SCORE_HISTORY
- **Seeded:** 400 rows manually inserted to seed initial snapshot. Alert manually executed to seed first alert entry.

### Step 6: Streamlit Dashboard -- SUPPLY_CHAIN_MONITOR
- **Status:** DONE
- **Session:** CoCo Session 1 (2026-10-16)
- **What:** Streamlit-in-Snowflake app with 5 sections:
  1. **Risk Overview** -- KPI metrics (critical/warning/healthy counts, total exposure, unmanaged risk gap) + risk distribution bar chart by tier
  2. **Supplier Scorecard** -- Filterable/sortable table with color-coded risk levels, all key metrics
  3. **At-Risk Purchase Orders** -- Filterable PO table sorted by dollar exposure
  4. **Supplier Deep Dive** -- Select a supplier for detail metrics + AI_COMPLETE risk summary button
  5. **Alert History** -- Log of fired alerts
- **Deployed to:** `@DEFAULT_DATABASE.PUBLIC.STREAMLIT_STAGE`
- **Local file:** `d:\HACKATHON\streamlit_app.py`

### Step 7: End-to-End Verification
- **Status:** DONE
- **Session:** CoCo Session 1 (2026-10-16)
- **Verified:**
  - SUPPLIER_QUALITY_SCORE: 400 rows, risk distribution looks correct
  - AT_RISK_PURCHASE_ORDERS: 14,434 rows, $182.8B exposure
  - Top risk supplier: Heritage Springs 42 (score 65.4, 42 safety-critical defects, TIER_3, PROBATION)
  - Alert: RESUMED and manually executed
  - Task: RESUMED and manually seeded
  - Streamlit: Deployed and accessible

---

## Grants Applied

These grants were needed because Dynamic Tables run as the owner role (ATTENDEE_ROLE), which did not have direct access to AUTO_MFG_DW via secondary roles.

```sql
GRANT USAGE ON DATABASE AUTO_MFG_DW TO ROLE ATTENDEE_ROLE;
GRANT USAGE ON ALL SCHEMAS IN DATABASE AUTO_MFG_DW TO ROLE ATTENDEE_ROLE;
GRANT SELECT ON ALL TABLES IN DATABASE AUTO_MFG_DW TO ROLE ATTENDEE_ROLE;
GRANT EXECUTE DATA METRIC FUNCTION ON ACCOUNT TO ROLE ATTENDEE_ROLE;
```

---

## Snowflake Features Used

| Feature | Where | Why |
|---|---|---|
| Dynamic Tables | SUPPLIER_QUALITY_SCORE, AT_RISK_PURCHASE_ORDERS | Continuously refreshed risk scoring pipeline |
| AI_CLASSIFY | SUPPLIER_QUALITY_SCORE | Categorize defect risk from free text descriptions |
| SENTIMENT | SUPPLIER_QUALITY_SCORE | Score customer complaint severity from warranty verbatims |
| AI_COMPLETE | Streamlit (on-demand) | Generate natural-language supplier risk summaries |
| Alert | SUPPLIER_RISK_ALERT | Proactive notification when critical risk thresholds crossed |
| Task | RISK_SCORE_SNAPSHOT | Daily snapshots for trend analysis |
| DMF | UNMANAGED_RISK_COUNT | Data quality metric measuring risk-action gap |
| Streamlit | SUPPLY_CHAIN_MONITOR | Visual dashboard for supply chain managers |

---

## What Remains

- [ ] Take screenshots of the Streamlit app for Devpost
- [ ] Record a short demo video (optional)
- [ ] Write the Devpost submission (project name, description, features, screenshots, honest bake score)
- [ ] Devpost deadline: **4:30 PM ET**
- [ ] Honest "How Baked Is It?" self-score: **3 (Working prototype)**

---

## Object Inventory

All objects live in `DEFAULT_DATABASE.PUBLIC`:

| Object Name | Type |
|---|---|
| SUPPLIER_QUALITY_SCORE | Dynamic Table |
| AT_RISK_PURCHASE_ORDERS | Dynamic Table |
| UNMANAGED_RISK_COUNT | Data Metric Function |
| SUPPLIER_RISK_ALERT | Alert |
| RISK_SCORE_SNAPSHOT | Task |
| ALERT_HISTORY | Table |
| RISK_SCORE_HISTORY | Table |
| STREAMLIT_STAGE | Stage |
| SUPPLY_CHAIN_MONITOR | Streamlit App |

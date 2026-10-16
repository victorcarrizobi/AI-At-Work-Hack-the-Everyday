# User Guide -- Supply Chain Risk Monitor

## Getting Started

Open the app in Snowsight:
1. Navigate to __Apps__ in the left sidebar
2. Click __Streamlit Apps__
3. Open __SUPPLY_CHAIN_MONITOR__

The app loads 4 cached queries on startup (5-minute TTL). First load may take a few seconds while the cache warms up.

---

## Theme Toggle

Click the sun icon (top-right corner) to switch between dark and light themes. All charts, cards, tables, and badges adapt automatically. The app defaults to dark mode.

---

## Tab 1: EXECUTIVE OVERVIEW

The landing page for executives who need a 30-second risk snapshot.

### Key Risk Indicators (top row)

| KPI | What It Means | Color Logic |
|---|---|---|
| Critical Suppliers | Suppliers with composite risk >= 58 | Red = high urgency |
| Warning Suppliers | Composite risk 38-57 | Yellow = monitor |
| Healthy Suppliers | Composite risk < 38 | Green = stable |
| At-Risk Exposure | Total dollar value of open POs from WARNING/CRITICAL suppliers | Purple = financial |
| Unmanaged Gap | WARNING/CRITICAL suppliers not yet SUSPENDED or on PROBATION | Red = action needed |

Hover over any KPI card to reveal its calculation methodology.

### Charts

- __Risk Distribution by Tier__: Stacked bar chart showing how many CRITICAL / WARNING / HEALTHY suppliers exist in each tier (TIER_1, TIER_2, TIER_3). Helps identify whether risk concentrates in a specific tier.
- __Top 10 Highest Risk Suppliers__: Bar chart of the 10 worst-scoring suppliers. Angled labels show supplier names.

### Exposure Summary with Top-N Selector

Use the "Show highest risk" dropdown to switch between Top 1, Top 5, Top 10, Top 100, or All suppliers. The three KPI cards and the supplier table below dynamically update to show:
- PO exposure for the selected group
- Number of at-risk POs
- Average risk score

Click __View in Explorer__ to pre-filter the DATA EXPLORER tab with the selected suppliers. An animated banner will appear telling you to click the DATA EXPLORER tab.

---

## Tab 2: MANAGER DASHBOARD

An operational view for supply chain managers who need to drill into specific suppliers and purchase orders.

### Supplier Scorecard

A full table of all 400 suppliers with these columns:

| Column | Description |
|---|---|
| SUPPLIER_NAME | Supplier identifier |
| SUPPLIER_TIER | TIER_1 (strategic), TIER_2 (preferred), TIER_3 (standard) |
| CURRENT_STATUS | ACTIVE, PROBATION, or SUSPENDED |
| RISK_LEVEL | CRITICAL, WARNING, or HEALTHY (color-coded) |
| COMPOSITE_RISK_SCORE | 0-100 (color-coded: red >= 58, yellow >= 38) |
| AI_RISK_SCORE | Average AI-classified defect severity |
| TOTAL_DEFECTS | Count of defect records |
| SAFETY_CRITICAL_DEFECTS | Defects classified as SAFETY_CRITICAL by AI |
| WARRANTY_CLAIMS | Count of warranty claims |
| AVG_CUSTOMER_SENTIMENT | -1 to +1 (negative = unhappy customers) |
| BASELINE_QUALITY_RATING | 0-100 from supplier master |
| ON_TIME_DELIVERY_PCT | Delivery reliability percentage |

Use the three filter dropdowns (Tier, Risk Level, Status) to narrow the view.

### At-Risk Purchase Orders

Shows the top 100 purchase orders by exposure from WARNING/CRITICAL suppliers. Filterable by risk level, sortable by exposure, risk score, or delivery date. Dollar exposure values over $10M appear in bold red; over $1M in yellow.

---

## Tab 3: SUPPLIER DEEP DIVE

An investigation view for analyzing a single supplier in depth.

1. Select a supplier from the dropdown (alphabetically sorted)
2. View the risk badge (CRITICAL / WARNING / HEALTHY) with tier and country
3. Review 8 KPI cards in a 4x2 grid:
   - Risk Score, AI Risk Score, Total Defects, Warranty Claims
   - Safety-Critical Defects, Avg Sentiment, On-Time Delivery, Quality Rating
4. Click __Generate AI Risk Summary__ to get a Cortex AI analysis (2-3 sentence summary with recommended action)
5. If the supplier has at-risk POs, they appear in a table at the bottom

The AI summary uses llama3.1-8b and takes 2-5 seconds to generate. It provides a natural-language interpretation of the numeric scores plus a specific recommended action.

---

## Tab 4: DATA EXPLORER

A power-user tab with 12 filters for slicing across all supplier and purchase order data.

### Filter Rows

__Row 1 (5 filters):__ Risk Level, Supplier Tier, Supplier Status, Part Category, PO Status

__Row 2 (5 filters):__ Destination Plant, Shipping Mode, Country, Risk Score Range (slider), Min Exposure ($)

__Row 3 (2 filters):__ Search Supplier Name (text), Search Part Name (text)

### Results

A summary bar shows: rows matched, unique suppliers, and total dollar exposure for the current filter combination.

The results table displays all matched rows with color-coded RISK_LEVEL and COMPOSITE_RISK_SCORE columns.

### Export Options

- __Export to Stage__: Writes filtered results as a CSV to `@STREAMLIT_STAGE/exports/`. Use `GET` from a SQL worksheet to download.
- __Show SQL Query__: Displays the equivalent SQL query. Copy it into a Snowsight SQL worksheet to run independently.

### Clear All Filters

Click the __Clear All Filters__ button (top right) to reset every filter to its default value.

---

## Tab 5: ALERTS & SYSTEM

### Alert History

Shows the last 50 alert firings in reverse chronological order. Each alert row includes:
- Timestamp
- Critical supplier count at time of firing
- Total at-risk exposure
- Top risk supplier name and score
- Human-readable message

If no alerts have fired in the current cycle, a "MONITORING ACTIVE" card appears explaining the 60-minute check interval.

### Pipeline Architecture

A reference table listing every Snowflake feature powering the monitor: Dynamic Tables, AI_CLASSIFY, SENTIMENT, AI_COMPLETE, Alert, Task, and DMF -- with a description of what each does.

---

## Interpreting Risk Scores

### Composite Risk Score (0-100)

| Range | Level | What to Do |
|---|---|---|
| 58-100 | CRITICAL | Investigate immediately. Consider suspending the supplier. Review safety-critical defects. Check if alternate suppliers exist. |
| 38-57 | WARNING | Schedule a review within the week. Monitor defect trends. Engage supplier quality team. |
| 0-37 | HEALTHY | Normal operations. No action required unless trends change. |

### Sentiment Score (-1 to +1)

| Range | Meaning |
|---|---|
| -1.0 to -0.3 | Strongly negative customer feedback. Likely product quality issues. |
| -0.3 to 0.0 | Mildly negative. Some customer dissatisfaction. |
| 0.0 to +0.5 | Neutral to mildly positive. |
| +0.5 to +1.0 | Positive feedback. |

### Unmanaged Gap

This KPI counts suppliers who are WARNING or CRITICAL but whose status is still ACTIVE (not PROBATION or SUSPENDED). A high unmanaged gap means the organization has identified risk but has not yet taken action. Target: 0.

---

## Data Refresh Cadence

| What | Frequency | Implication |
|---|---|---|
| Dynamic Tables | Every 1 hour | KPIs, charts, and tables reflect data within the last hour |
| Alert | Every 60 minutes | Critical-risk notifications within 1 hour of detection |
| Risk Score Snapshot | Daily at 6 AM ET | Historical trends available for next-day analysis |
| Streamlit Cache | 5-minute TTL | Within any session, data refreshes every 5 minutes |

# Build Journal -- Supply Chain Risk Monitor

How a production-grade supply chain risk monitor was built from scratch in a single hackathon day using Snowflake and CoCo.

---

## The Starting Point

__Event:__ Data in the D 2026 Hackathon, Detroit, MI
__Track:__ Hack the Grind (build repeat-use tools for engineers)
__Time:__ One day, deadline 4:30 PM ET
__Tools:__ Snowflake (Dynamic Tables, Cortex AI, Streamlit) + CoCo (Cortex Code Desktop)

The hackathon provided three challenge datasets: automotive manufacturing (AUTO_MFG_DW), financial services (FINSERV_DW), and healthcare (HEALTHCARE_DW). We picked automotive -- Detroit is car country, and the data had the richest cross-table relationships.

---

## The Idea

Supply chain managers drown in spreadsheets. They have defect reports in one system, warranty claims in another, purchase orders in a third. Nobody has a single view that answers: "Which suppliers are putting us at risk right now, and how much money is exposed?"

We would build a monitor that:
1. Scores every supplier automatically using AI on their defect and warranty data
2. Flags at-risk purchase orders tied to bad suppliers
3. Alerts when critical risk goes unmanaged
4. Gives supply chain managers one place to see everything

---

## The Build: Seven Steps

### Step 1 -- The Brain (Dynamic Table: SUPPLIER_QUALITY_SCORE)

The first and most important object. A single Dynamic Table that joins four source tables (suppliers, defects, warranty claims, purchase orders) and applies two Cortex AI functions:

- __AI_CLASSIFY__ reads 8,000 defect descriptions and categorizes each as SAFETY_CRITICAL, PERFORMANCE, COSMETIC, or WEAR_AND_TEAR
- __SENTIMENT__ scores 30,000 warranty customer complaints from -1 (angry) to +1 (happy)

These feed into a composite risk formula:

```
30% AI defect severity
+ 20% defect volume
+ 20% inverse quality rating
+ 15% warranty volume
+ 15% negative customer sentiment
= Score out of 100
```

Result: 400 suppliers scored. The first run revealed 20 CRITICAL, 268 WARNING, 112 HEALTHY. Heritage Springs 42 topped the list with a 65.4 risk score and 42 safety-critical defects.

__GOTCHA:__ We used CURRENT_TIMESTAMP() for a "last refreshed" column. This forced Snowflake into full-refresh mode, re-running AI_CLASSIFY and SENTIMENT on every refresh cycle. For the hackathon it is acceptable. In production, move the timestamp to a view.

### Step 2 -- The Exposure Map (Dynamic Table: AT_RISK_PURCHASE_ORDERS)

A second Dynamic Table that chains off the first. It joins open purchase orders (PENDING, CONFIRMED, SHIPPED) against supplier risk scores and calculates dollar exposure per PO (quantity times unit price).

Result: 14,434 at-risk purchase orders totaling $182.8B in exposure.

The two Dynamic Tables form a chain: when source data changes, DT1 refreshes first, then DT2 picks up the new scores. Both run on a 1-hour TARGET_LAG.

### Step 3 -- The Quality Metric (Data Metric Function)

We created UNMANAGED_RISK_COUNT -- a custom DMF that measures the gap between suppliers identified as risky and suppliers where action has been taken (SUSPENDED or PROBATION).

__GOTCHA:__ The DMF function was created and works manually, but ALTER TABLE ADD DATA METRIC FUNCTION failed with "Function does not exist or not authorized." After four different attempts (ownership grants, EXECUTE DATA METRIC FUNCTION grants, column name matching), we concluded this was a trial account limitation. We embedded the equivalent logic directly in the Streamlit app.

### Step 4 -- The Watchdog (Alert + Task)

- __Alert (SUPPLIER_RISK_ALERT):__ Checks every 60 minutes. If CRITICAL-risk suppliers are not SUSPENDED or on PROBATION, it fires and logs to ALERT_HISTORY. This is the "someone should be looking at this" signal.

- __Task (RISK_SCORE_SNAPSHOT):__ Runs daily at 6 AM Eastern. Snapshots all 400 supplier risk scores into RISK_SCORE_HISTORY for trend tracking. Today's CRITICAL supplier might have been WARNING last week -- the snapshot captures that trajectory.

### Step 5 -- The First Big Gotcha

Dynamic Tables, Tasks, and Alerts all run as the owner role. Our owner role (ATTENDEE_ROLE) had access to the challenge database through ACCOUNTADMIN as a secondary role -- but secondary roles are not applied during object execution.

The fix was three GRANT statements. Simple, but it cost 15 minutes of debugging because the error message ("Database does not exist or not authorized") does not mention secondary roles. This became GOTCHA-001 in our documentation.

### Step 6 -- The Dashboard (Streamlit-in-Snowflake)

The Streamlit app went through three iterations across multiple CoCo sessions:

__Version 1:__ Four tabs (Executive Overview, Manager Dashboard, Supplier Deep Dive, Alerts and System) with basic st.bar_chart calls and st.dataframe tables. Got the data flowing end-to-end.

__Version 2:__ Added the 5th tab (DATA EXPLORER) with 12 filters, CSV export, and Show SQL. Added session state management and conditional formatting. Replaced basic charts with Vega-Lite specs for theme-aware rendering. Added dark/light theme toggle.

__Version 3:__ Added Top-N selector to Executive Overview (Top 1/5/10/100/All). Added "View in Explorer" cross-tab navigation with animated pulse-border banner. Replaced CSV download with "Export to Stage" via COPY INTO. Added AI_COMPLETE on-demand summaries for supplier deep dives.

### Step 7 -- QA

A full end-to-end QA walkthrough tested all tabs, every filter, every button:
- Found 2 crash bugs (deprecated Streamlit API: st.experimental_rerun)
- Found a slider that would create a float instead of a range tuple
- Found the bar charts were incompatible with the Snowflake Streamlit runtime
- Found the deployed code was out of sync with the local file

All issues cataloged in QA-DEFECTS.md with severity ratings, exact line numbers, and fix instructions.

---

## Design Decisions and Trade-offs

__Why Dynamic Tables over scheduled Tasks?__
Dynamic Tables handle the DAG orchestration automatically -- DT2 waits for DT1. With Tasks, we would need to manage execution order manually. Dynamic Tables also mean zero ETL code; the pipeline is pure SQL.

__Why AI_CLASSIFY over regex/rules?__
Defect descriptions are free-text: "Intermittent brake shudder at highway speeds" versus "Minor paint chip on interior trim." AI_CLASSIFY handles nuance that regex cannot. The four-category classification (SAFETY_CRITICAL, PERFORMANCE, COSMETIC, WEAR_AND_TEAR) maps naturally to risk severity.

__Why a composite score instead of just using AI_CLASSIFY?__
A supplier might have a few severe defects but excellent delivery and quality ratings. The composite score blends multiple signals so a single metric does not dominate. The weights (30/20/20/15/15) were chosen to prioritize AI-detected severity while keeping other metrics meaningful.

__Why Streamlit-in-Snowflake instead of a standalone app?__
Zero deployment friction. No server to manage. The app runs inside Snowflake, reads from Dynamic Tables directly, and inherits the user's role/permissions. For a hackathon, this eliminates an entire category of setup problems.

__Why full refresh instead of incremental?__
CURRENT_TIMESTAMP() forces full refresh. We accepted this trade-off because the timestamp makes the "last refreshed" display meaningful to users. In production, the fix is straightforward: remove the timestamp from the DT and add it in a view or the Streamlit layer.

---

## What CoCo Did

CoCo (Cortex Code Desktop) was used for the entire build -- from data exploration through deployment. Specific contributions:

- Explored all 22 databases in the hackathon account, sampled all three challenge datasets, and recommended the project idea
- Planned and built the 7-step pipeline with real-time error handling (7 gotchas documented)
- Wrote all SQL DDL (Dynamic Tables, Alert, Task, DMF, Grants)
- Built the 700+ line Streamlit app across three iterations
- Performed QA walkthrough via browser automation (4 tabs tested, 10 defects cataloged)
- Created all documentation (PROGRESS.md, LOG.md, GOTCHA.md, QA-DEFECTS.md, ARCHITECTURE.md, USER-GUIDE.md)
- Set up GitHub repo and managed the full git workflow
- Wrote all Devpost submission content

---

## Snowflake Features Used

| Feature | Count/Scale | Purpose |
|---|---|---|
| Dynamic Tables | 2 (chained) | Continuous risk scoring pipeline |
| AI_CLASSIFY | 8,000 classifications | Defect severity from free text |
| SENTIMENT | 30,000 scores | Customer complaint severity |
| AI_COMPLETE | On-demand | Natural-language risk summaries |
| Alert | 1 (60-min schedule) | Unmanaged critical risk detection |
| Task | 1 (daily CRON) | Historical trend snapshots |
| Data Metric Function | 1 | Risk-action gap measurement |
| Streamlit-in-Snowflake | 1 app, 5 tabs | Full dashboard |

---

## If We Had More Time

1. __Incremental refresh:__ Remove CURRENT_TIMESTAMP() from DT1 to enable incremental mode. This would reduce AI function costs by ~95% per refresh cycle.
2. __Trend charts:__ Use RISK_SCORE_HISTORY to show how each supplier's risk evolved over time. The data is being collected; it just needs a visualization.
3. __Notification integration:__ Wire the Alert to email or Slack instead of just logging to a table.
4. __Role-based views:__ Different dashboards for executives (aggregated) versus analysts (detailed) versus procurement (PO-focused).
5. __Supplier action workflow:__ Buttons to move suppliers to PROBATION or SUSPENDED status directly from the dashboard, updating the source data and triggering a DT refresh.

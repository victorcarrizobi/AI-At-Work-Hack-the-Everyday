# Video Script -- Supply Chain Risk Monitor
## Data in the D 2026 Hackathon | Hack the Grind Track
### STAR Methodology | Target: 3:30 - 4:00 minutes

---

## INTRO (20 sec)

**Visual:** Title card -- "SUPPLY CHAIN RISK MONITOR" with dark theme background, Snowflake + Cortex AI logos

**Speaker:**
"Hey everyone, my name is Victor and this is Supply Chain Risk Monitor -- an AI-powered pipeline I built during the Data in the D 2026 Hackathon on the Hack the Grind track. In the next few minutes I'm going to walk you through the problem, why it matters, what I built, and the results -- all running live on Snowflake with real data."

---

## SITUATION -- The Problem (45 sec)

**Visual:** Slide with factory/supply chain imagery. Key stats appear as speaker mentions them: 400 suppliers, 50,000 POs, 8,000 defects, 30,000 warranty complaints. Transition to a "quarterly review" calendar graphic showing the delay gap.

**Speaker:**
"Imagine you're a supply chain manager at an automotive manufacturer in Detroit. You oversee 400 suppliers across three tiers. One of them -- let's call them Heritage Springs -- makes brake pad components. Their defect rate has been climbing for months. Customers are writing angry warranty complaints. But you don't know yet -- because your quality data lives in spreadsheets, your warranty data lives in a different system, and your purchasing team reviews suppliers once a quarter.

By the time the quarterly review happens, Heritage Springs has shipped 42 safety-critical defects, generated 84 warranty claims, and your company is exposed on over a thousand open purchase orders.

That's the reality for most manufacturers today. The data exists -- defect reports, warranty complaints, supplier ratings, purchase orders -- but nobody is connecting the dots in real time."

---

## TASK -- What We Need (30 sec)

**Visual:** Slide with 4 bullet points appearing one by one: (1) Continuously monitor 400 suppliers, (2) Use AI to analyze unstructured text, (3) Score every supplier on a single risk index, (4) Alert the team before crisis. Bottom line: "All on Snowflake. No external infrastructure. Fully autonomous."

**Speaker:**
"So the task was clear: Can we build a system that continuously monitors all 400 suppliers, uses AI to analyze the unstructured data -- the defect descriptions, the customer complaints -- scores every supplier on a single risk index, flags the at-risk purchase orders, and alerts the team before it becomes a crisis?

And can we do it entirely on Snowflake, with no external infrastructure, running autonomously without someone pressing refresh every morning?"

---

## ACTION -- What I Built (90 sec)

**Visual:** Architecture diagram showing the data flow: AUTO_MFG_DW sources --> AI_CLASSIFY + SENTIMENT --> SUPPLIER_QUALITY_SCORE (DT) --> AT_RISK_PURCHASE_ORDERS (DT) --> Alert + Task --> Streamlit Dashboard. Animate each step as the speaker describes it. Then transition to live screen recording of the dashboard.

**Speaker:**
"Here's what I built -- entirely on Snowflake in a single session.

The pipeline starts with the AUTO_MFG_DW challenge database -- 14 tables, real manufacturing data. I feed 8,000 defect descriptions through Cortex AI_CLASSIFY, which categorizes each one as Safety-Critical, Performance, Cosmetic, or Wear and Tear. Then I run SENTIMENT analysis on 30,000 customer warranty complaints to score how severe each one is.

These AI outputs combine with defect volumes, quality ratings, and warranty claim counts into a composite risk score -- a single number from 0 to 100 for every supplier. The formula weights AI-classified risk at 30%, defect volume at 20%, inverse quality rating at 20%, warranty claims at 15%, and negative sentiment at 15%.

All of this runs inside Dynamic Tables that refresh automatically every hour. No cron jobs, no ETL scripts -- Snowflake handles the orchestration.

On top of that, I have an Alert that fires every 60 minutes checking for critical-risk suppliers that haven't been actioned yet, and a Task that snapshots risk scores daily for trend tracking.

The dashboard is a Streamlit-in-Snowflake app with five tabs. Executives see KPI cards and risk distribution charts with a Top-N exposure selector. Managers get filterable scorecards and at-risk purchase order tables. Power users get a 12-filter Data Explorer with CSV export. And on any supplier, you can click one button and Cortex AI_COMPLETE generates a natural-language risk summary -- not a canned template, an actual AI analysis of that specific supplier's risk profile.

The app has a dark and light theme with smooth transitions, hover tooltips explaining every metric, and cross-tab navigation so you can drill from executive overview straight into filtered detail data."

**Screen Recording Notes:**
- Show Executive Overview tab: KPI cards, charts
- Click Top 5, then "View in Explorer" to show cross-tab navigation
- Switch to Data Explorer: apply a filter, show results updating
- Go to Supplier Deep Dive: select a critical supplier, click "Generate AI Summary"
- Toggle theme from dark to light and back

---

## RESULT -- What We Got (45 sec)

**Visual:** Results slide with big numbers animating in: 33 CRITICAL (red), 294 WARNING (yellow), 73 HEALTHY (green). Then 16,408 at-risk POs. Then "11 gotchas documented." Then the 8 Snowflake feature icons.

**Speaker:**
"The results speak for themselves. Out of 400 suppliers, the pipeline identified 33 as Critical risk -- averaging 43 defects each and a sentiment score deep in the negative. 294 are flagged as Warning. Only 73 are Healthy.

The system flagged 16,408 at-risk purchase orders -- that's real dollar exposure that a supply chain manager can act on today.

Everything is real. No mocked data, no hardcoded numbers. The AI is doing actual work -- classifying real defect text, scoring real customer complaints. The pipeline refreshes itself. The alert monitors continuously.

I hit 11 gotchas during the build -- from Dynamic Table role permissions to AI model deprecation to Streamlit compatibility issues in the Snowflake environment. Every one is documented."

---

## CLOSE (20 sec)

**Visual:** Final slide -- "How Baked Is It? Score: 4 (Usable by Others)" with the 8 Snowflake features listed as icons. Project name, hackathon name, "Built with Cortex Code" badge. QR code or link to GitHub repo.

**Speaker:**
"I scored this a 4 out of 5 on the 'How Baked Is It' scale -- Usable by Others. It handles bad input, shows clear error messages, and a supply chain manager who has never seen the code could open this dashboard and make decisions today.

This is Supply Chain Risk Monitor. Eight Snowflake features working together intentionally -- not a checklist, a pipeline. Built with Cortex Code during Data in the D 2026. Thank you."

---

## REFERENCE DATA FOR VIDEO PRODUCTION

### Key Stats to Display
- 400 suppliers monitored (Tier 1, 2, 3)
- 8,000 defect descriptions analyzed by AI_CLASSIFY
- 30,000 warranty complaints scored by SENTIMENT
- 50,000 purchase orders tracked
- 33 CRITICAL / 294 WARNING / 73 HEALTHY risk distribution
- 16,408 at-risk purchase orders flagged
- 11 gotchas documented and solved
- 8 Snowflake features used intentionally

### Composite Risk Formula (for architecture slide)
- 30% AI-classified defect risk (AI_CLASSIFY)
- 20% Defect volume (capped at 50)
- 20% Inverse quality rating (from supplier master)
- 15% Warranty claim volume (capped at 200)
- 15% Negative customer sentiment (SENTIMENT)

### Snowflake Features (for features slide)
1. Dynamic Tables (SUPPLIER_QUALITY_SCORE, AT_RISK_PURCHASE_ORDERS)
2. AI_CLASSIFY (defect risk categorization)
3. SENTIMENT (warranty complaint scoring)
4. AI_COMPLETE (on-demand risk summaries)
5. Alert (SUPPLIER_RISK_ALERT -- 60 min cycle)
6. Task (RISK_SCORE_SNAPSHOT -- daily 6 AM ET)
7. DMF (UNMANAGED_RISK_COUNT)
8. Streamlit (SUPPLY_CHAIN_MONITOR -- 5 tabs, dark/light theme)

### Risk Thresholds
- CRITICAL: score >= 58 (33 suppliers, avg 43.5 defects, avg score 60.4)
- WARNING: score >= 38 (294 suppliers, avg 20.7 defects, avg score 46.8)
- HEALTHY: score < 38 (73 suppliers, avg 6.5 defects, avg score 33.8)

### Color Palette (for slide design)
- Dark theme: #0F172A (bg), #22C55E (accent green), #FCA5A5 (critical), #FDE68A (warning), #86EFAC (healthy)
- Light theme: #EFF2F7 (bg), #16A34A (accent), #B91C1C (critical), #B45309 (warning), #15803D (healthy)

### App URL
- Streamlit: SUPPLY_CHAIN_MONITOR in DEFAULT_DATABASE.PUBLIC
- GitHub: https://github.com/victorcarrizobi/AI-At-Work-Hack-the-Everyday

### Timing Summary
| Section | Duration | Cumulative |
|---------|----------|------------|
| Intro | 20 sec | 0:20 |
| Situation | 45 sec | 1:05 |
| Task | 30 sec | 1:35 |
| Action | 90 sec | 3:05 |
| Result | 45 sec | 3:50 |
| Close | 20 sec | 4:10 |

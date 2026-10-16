# NOTE FOR JUDGES -- Supply Chain Risk Monitor

## Data in the D 2026 Hackathon | Hack the Grind Track

---

## Project Summary

**Supply Chain Risk Monitor** is an AI-powered, real-time supplier quality scoring and risk detection pipeline built entirely on Snowflake. It continuously scores 400 auto manufacturing suppliers using AI-classified defect analysis and customer sentiment, flags at-risk purchase orders, and alerts supply chain managers when critical thresholds are crossed -- all through a dark/light themed Streamlit dashboard with 5 tabs serving both executives and operational managers.

---

## What Makes This Project Different

1. **AI is doing real work, not decoration.** AI_CLASSIFY categorizes 8,000 defect descriptions into risk categories. SENTIMENT scores 30,000 customer verbatim complaint texts. AI_COMPLETE generates natural-language risk summaries on demand. These aren't cosmetic -- they drive the composite risk score formula.

2. **The pipeline runs itself.** Dynamic Tables refresh automatically. The Alert fires every 60 minutes. The Task snapshots daily. A supply chain manager opens the dashboard and sees current risk -- no manual refresh, no stale data.

3. **Dual-audience design.** Executive Overview for C-suite (KPI cards, charts, top-N exposure selector). Manager Dashboard for operational staff (filterable scorecards, PO tables). Data Explorer for power users (12 filters, SQL export, CSV stage export).

---

## Build Timeline (Single Session -- ~3 hours)

| Time (ET) | Action | Outcome |
|---|---|---|
| 1:15 PM | Project kickoff | Explored 22 databases, 3 challenge datasets. Chose AUTO_MFG_DW for Detroit/auto thematic fit |
| 1:18 PM | Plan created | 7-step architecture plan approved. DT -> Alert -> Task -> Streamlit |
| 1:19 PM | Grants applied | Fixed DT owner-role access issue (GOTCHA-001). ATTENDEE_ROLE granted direct access to AUTO_MFG_DW |
| 1:20 PM | DT: SUPPLIER_QUALITY_SCORE | AI_CLASSIFY + SENTIMENT + composite scoring. 400 suppliers scored |
| 1:22 PM | DT: AT_RISK_PURCHASE_ORDERS | 16,408 at-risk POs flagged with dollar exposure |
| 1:22 PM | DMF: UNMANAGED_RISK_COUNT | Created. Auto-attach failed (trial account limitation) |
| 1:24 PM | Alert + Task | SUPPLIER_RISK_ALERT (60 min) + RISK_SCORE_SNAPSHOT (daily 6 AM ET) |
| 1:28 PM | Streamlit v1 | Basic 5-section single-page app deployed |
| 1:30 PM | Documentation | Created PROGRESS.md, LOG.md, GOTCHA.md for multi-session collaboration |
| 1:35 PM | Graphify analysis | Knowledge graph: 90 nodes, 79 edges, 31 communities across all project files |
| 1:40 PM | Skills installed | graphify, caveman, ponytail, superpowers, ui-ux-pro-max (29 skills total) |
| 2:00 PM | UI/UX Pro Max redesign | Dark command center theme, 4 tabs, glassmorphism cards, KPI upgrade |
| 2:15 PM | Chart fix | st.bar_chart color param not supported in SiS. Removed |
| 2:20 PM | Full audit | 5 issues found and fixed: thresholds, alert alignment, error handling, PO limits, counts |
| 2:30 PM | Threshold tightening | CRITICAL >= 58, WARNING >= 38 (was 60/40). More defensible distribution |
| 2:45 PM | Theme toggle | Sun/moon icon, CSS transitions, light theme redesigned with UI/UX Pro guidance |
| 3:00 PM | Data Explorer tab | 12 filters, CSV export, SQL query display, Clear All Filters button |
| 3:15 PM | Top-N selector | Top 1/5/10/100/All with "View in Explorer" navigation + animated banner |
| 3:30 PM | Hover tooltips | All 13 KPI cards show methodology on hover |
| 3:45 PM | Export fix | Replaced broken st.download_button with COPY INTO stage + SQL query approach |
| 4:00 PM | Vega-Lite charts | Theme-aware charts with transparent backgrounds matching light/dark mode |

---

## Iteration History and Design Decisions

### Decision 1: Why AUTO_MFG_DW?
- Three challenge datasets: AUTO_MFG_DW, FINSERV_DW, HEALTHCARE_DW
- AUTO_MFG_DW chosen for: Detroit thematic fit ("Data in the D"), rich free-text fields (defect descriptions, customer verbatim), clear supply chain relationships
- 14 tables across 4 schemas: PRODUCT, QUALITY, SALES, SUPPLY_CHAIN, WORKFORCE

### Decision 2: Why Hack the Grind?
- Platform Craft is 30% of the grade -- highest weight of any criterion
- The project uses 8 Snowflake features working together intentionally
- A pipeline that runs itself = "Time Reclaimed" (15%) is a natural fit

### Decision 3: Composite Risk Score Formula
- 30% AI-classified defect risk (AI_CLASSIFY on free text)
- 20% Defect volume (capped at 50)
- 20% Inverse quality rating (from supplier master)
- 15% Warranty claim volume (capped at 200)
- 15% Negative customer sentiment (SENTIMENT on verbatim text)
- Validated by recalculating top 5 suppliers -- stored values match manual recalculation exactly

### Decision 4: Threshold Tightening (Audit Finding)
- Original: CRITICAL >= 60, WARNING >= 40
- Problem: HEALTHY suppliers could have 25 defects and -0.47 sentiment
- Fixed: CRITICAL >= 58, WARNING >= 38
- Result: 33 CRITICAL (avg 43.5 defects), 294 WARNING, 73 HEALTHY (avg 6.5 defects)

### Decision 5: UI/UX Pro Max Design System
- Queried the design system tool for "industrial supply chain dashboard dark command center"
- Received: Glassmorphism style, dark tech palette (#0F172A bg, #22C55E accent), Fira Code/Fira Sans fonts, dense dashboard density (8/10)
- Light theme validated separately: Minimalism & Swiss Style, cool slate background (#EFF2F7), stronger contrast colors for accessibility (4.5:1 minimum)

---

## Gotchas Encountered (13 total)

| # | Issue | Impact | Resolution |
|---|---|---|---|
| 1 | Dynamic Tables can't use secondary roles | DT refresh failed | Granted direct access to ATTENDEE_ROLE |
| 2 | DMF auto-attach fails | "Function not authorized" | DMF created manually; logic embedded in app |
| 3 | AI_COMPLETE model deprecation | snowflake-llama-3.3-70b, llama4-maverick deprecated | llama3.1-8b confirmed working |
| 4 | PARTS_CATALOG.PRIMARY_SUPPLIER_ID is company code | Wrong join path | Join through PURCHASE_ORDERS instead |
| 5 | pandas applymap deprecated | SiS uses newer pandas | Replaced with style.map() |
| 6 | Streamlit stage must exist before CREATE STREAMLIT | Deploy failed | Create stage first, upload, then create |
| 7 | CURRENT_TIMESTAMP forces FULL refresh | Expensive AI re-runs | Acceptable for hackathon; removed from DT in v2 |
| 8 | st.bar_chart color= not supported in SiS | TypeError on load | Switched to st.vega_lite_chart |
| 9 | st.download_button S3 SignatureDoesNotMatch | Export broken | Replaced with COPY INTO stage + SQL query |
| 10 | Clear Filters session state conflict | "default value but also session state" error | Removed default= args, use session state only |
| 11 | Slider returns float instead of tuple | TypeError on subscript | Pre-initialize session state as tuple |
| 12 | HEADER = TRUE invalid inside FILE_FORMAT | COPY INTO export failed | Moved HEADER to top-level COPY option |
| 13 | st.rerun() does NOT exist in SiS | AttributeError crash | Use st.experimental_rerun() instead |

---

## Data Quality Audit Results

| Check | Result |
|---|---|
| Orphan suppliers (DT vs source) | 0 |
| NULL risk scores | 0 |
| Scores out of range (0-100) | 0 |
| Invalid risk levels | 0 |
| Missing supplier names | 0 |
| Sentiment out of range (-1 to 1) | 0 |
| Warranty join duplicates (fanout) | 0 (30,000 = 30,000 distinct) |
| AT_RISK_PO null suppliers | 0 |
| AT_RISK_PO zero/negative exposure | 0 |
| Alert state | STARTED (active) |
| Task state | STARTED (active) |

---

## Snowflake Features Used (8 features, intentional composition)

| Feature | Object | Why It's Here |
|---|---|---|
| Dynamic Tables | SUPPLIER_QUALITY_SCORE, AT_RISK_PURCHASE_ORDERS | Continuously refreshed risk pipeline -- no manual ETL |
| AI_CLASSIFY | Inside SUPPLIER_QUALITY_SCORE | Categorizes 8,000 defect descriptions into risk categories from free text |
| SENTIMENT | Inside SUPPLIER_QUALITY_SCORE | Scores 30,000 warranty customer verbatim texts |
| AI_COMPLETE | Streamlit on-demand | Generates natural-language risk summaries per supplier |
| Alert | SUPPLIER_RISK_ALERT | Proactive notification when critical-risk suppliers remain unactioned |
| Task | RISK_SCORE_SNAPSHOT | Daily trend snapshots for historical analysis |
| DMF | UNMANAGED_RISK_COUNT | Data quality metric measuring risk-action gap |
| Streamlit | SUPPLY_CHAIN_MONITOR | 5-tab dashboard with dark/light theme, 12 filters, export |

---

## Object Inventory (DEFAULT_DATABASE.PUBLIC)

| Object | Type | Rows | Status |
|---|---|---|---|
| SUPPLIER_QUALITY_SCORE | Dynamic Table | 400 | Refreshing (1hr lag) |
| AT_RISK_PURCHASE_ORDERS | Dynamic Table | 16,408 | Refreshing (1hr lag) |
| UNMANAGED_RISK_COUNT | Data Metric Function | N/A | Created (manual call) |
| SUPPLIER_RISK_ALERT | Alert | N/A | RESUMED (60 min) |
| RISK_SCORE_SNAPSHOT | Task | N/A | RESUMED (daily 6AM ET) |
| ALERT_HISTORY | Table | 0 | Alert log target |
| RISK_SCORE_HISTORY | Table | 400 | Trend snapshots |
| STREAMLIT_STAGE | Stage | N/A | App + export storage |
| SUPPLY_CHAIN_MONITOR | Streamlit App | N/A | Deployed |

---

## Streamlit App Architecture (5 Tabs)

### Tab 1: Executive Overview
- 5 KPI cards with hover tooltips explaining methodology
- 2 Vega-Lite charts (Risk by Tier, Top 10 Risk Suppliers) -- theme-aware
- Top-N selector (Top 1/5/10/100/All) with dynamic KPIs and supplier table
- "View in Explorer" button with animated navigation banner

### Tab 2: Manager Dashboard
- Filterable supplier scorecard (Tier, Risk Level, Status)
- Conditional formatting on risk level and composite score
- At-risk PO table with dollar exposure highlighting

### Tab 3: Supplier Deep Dive
- Select any supplier for 8-metric detail view
- Risk badge + all KPI cards with hover methodology
- AI_COMPLETE risk summary button (Cortex AI generates 2-3 sentence analysis)
- Per-supplier PO table

### Tab 4: Data Explorer
- 12 filters across 3 rows (multiselects, slider, number input, text search)
- Clear All Filters button
- Pre-filterable from Executive "View in Explorer" flow
- Export to Stage (COPY INTO) + Show SQL Query
- Results summary (row count, supplier count, exposure total)

### Tab 5: Alerts & System
- Alert history table
- Pipeline architecture reference (all 7 Snowflake features documented)
- Data source inventory

---

## Design System Applied

### Dark Mode (Default)
- Background: #0F172A (deep navy)
- Cards: Glassmorphism with #1E293B -> #1B2336 gradient
- Accent: #22C55E (status green)
- Risk colors: #FCA5A5 (critical), #FDE68A (warning), #86EFAC (healthy)

### Light Mode
- Background: #EFF2F7 (cool slate, NOT pure white per UX guidance)
- Cards: White with subtle box-shadow for depth
- Risk colors: Darker variants for 4.5:1 contrast (#B91C1C, #B45309, #15803D)
- Smooth 0.3s CSS transition between themes

### Theme Toggle
- Sun icon (dark mode) / Moon icon (light mode)
- All charts, cards, text, and borders adapt dynamically

---

## "How Baked Is It?" Self-Score: 4 (Usable by Others)

### What's Real (everything)
- All data flows from AUTO_MFG_DW through AI functions into Dynamic Tables -- no mocked data anywhere
- Alert fires on schedule with real conditions (60-minute cycle, RESUMED)
- Task snapshots run daily at 6 AM ET (RESUMED)
- Dashboard reads live data with 5-minute caching
- AI_COMPLETE generates real risk summaries per supplier using llama3.1-8b
- Export works via COPY INTO stage with header row + SQL query fallback
- Dark/light theme with smooth CSS transitions

### What Earns a 4 (handles bad input, usable by someone who isn't the builder)
- **Error handling on data load:** All four data queries wrapped in try/except with user-friendly error messages. If Snowflake is unreachable or DTs are still refreshing, the app shows a clear message instead of a stack trace.
- **Empty state handling:** If no supplier data exists, or if no at-risk POs exist, or if filters return zero results, the app shows contextual warnings instead of blank/broken pages.
- **Loading spinner:** Initial data load shows a progress spinner so users know the app is working.
- **Input sanitization:** Text search fields escape single quotes before embedding in COPY INTO SQL to prevent query breakage.
- **Graceful AI fallback:** AI_COMPLETE calls wrapped in try/except -- if the model is unavailable, users get a fallback message suggesting manual review.
- **Session state safety:** All filter widgets use session state initialization patterns to prevent type mismatches (slider tuple bug fixed, Clear All Filters properly resets).
- **12-filter Data Explorer:** Users can combine filters freely, see result counts in real time, and export filtered data. Clear All Filters resets everything.
- **Cross-tab navigation:** "View in Explorer" sets filter state and shows an animated banner guiding users to the right tab.
- **Theme-aware charts:** Vega-Lite charts with transparent backgrounds adapt to dark/light mode automatically.
- **Hover tooltips on all KPIs:** Every metric card explains how the number was calculated.

### What Would Make It a 5 (Handoff-Ready)
- Role-based access control on the Streamlit app (executive vs. manager views gated by role)
- Automated remediation workflows (create tickets, suspend suppliers automatically)
- Email/Slack/PagerDuty notification integration on Alert trigger
- Multi-day trend charts with regression analysis (needs more daily snapshots)
- Input validation on all filter combinations (some edge cases with very large result sets)
- Comprehensive unit and integration tests

### Honest Assessment
A strong 4. The app handles bad input, shows clear error messages, and could be used by a supply chain manager who has never seen the code. Every data point is real, every AI call processes actual text, and the pipeline refreshes itself. The gap to a 5 is operational hardening: RBAC, automated remediation, and notification integrations that a hackathon environment can't fully demonstrate.

---

## Tools and Skills Used During Build

| Tool/Skill | Purpose |
|---|---|
| CoCo (Cortex Code) claude-opus-4-6 | Primary AI assistant for all code, SQL, and architecture |
| sql-author skill | SQL validation and best practices |
| developing-with-streamlit-in-snowflake skill | SiS deployment guidance |
| ui-ux-pro-max skill | Design system generation, color audit, UX guidelines |
| graphify skill | Knowledge graph of project (90 nodes, 79 edges) |
| html-authoring skill | CSS/HTML guidance for custom Streamlit components |

---

## Source Data Summary (AUTO_MFG_DW)

| Table | Schema | Rows | Used For |
|---|---|---|---|
| SUPPLIERS | SUPPLY_CHAIN | 400 | Supplier master data, quality ratings |
| DEFECTS | QUALITY | 8,000 | AI_CLASSIFY risk categorization |
| WARRANTY_CLAIMS | QUALITY | 30,000 | SENTIMENT analysis on verbatim text |
| PURCHASE_ORDERS | SUPPLY_CHAIN | 50,000 | Dollar exposure, supplier-part linkage |
| PARTS_CATALOG | PRODUCT | 3,000 | Part names and categories |
| INSPECTIONS | QUALITY | 25,000 | (Available, not used in final scoring) |

---

## Grants Applied

```sql
GRANT USAGE ON DATABASE AUTO_MFG_DW TO ROLE ATTENDEE_ROLE;
GRANT USAGE ON ALL SCHEMAS IN DATABASE AUTO_MFG_DW TO ROLE ATTENDEE_ROLE;
GRANT SELECT ON ALL TABLES IN DATABASE AUTO_MFG_DW TO ROLE ATTENDEE_ROLE;
GRANT EXECUTE DATA METRIC FUNCTION ON ACCOUNT TO ROLE ATTENDEE_ROLE;
```

---

## Files in Repository

| File | Purpose |
|---|---|
| streamlit_app.py | Main Streamlit application (830 lines) |
| PROGRESS.md | Step-by-step build tracker (18 steps across 4 sessions) |
| LOG.md | Chronological session log across 4 CoCo sessions |
| GOTCHA.md | 12 documented pitfalls with fixes |
| NOTE4JUDGES.md | This document |
| EXECUTIVE_SUMMARY.docx | Executive summary for stakeholders |
| TECHNICAL_ARCHITECTURE.docx | Deep technical architecture document |
| VIDEO_SCRIPT.md | STAR-method video script (3:30-4:00 min) |
| QA-DEFECTS.md | QA walkthrough -- all P0s resolved |
| ARCHITECTURE.md | Technical deep dive: data flow, DDL, scoring |
| USER-GUIDE.md | How to use the app: tabs, KPIs, filters, export |
| BUILD-JOURNAL.md | Narrative build story: decisions, gotchas, trade-offs |
| Supply_Chain_Risk_Monitor.pptx | PowerPoint presentation |
| PPT/HACKATHON-HANDOFF.md | Original hackathon brief |
| graphify-out/ | Knowledge graph outputs (HTML, JSON, Obsidian vault) |

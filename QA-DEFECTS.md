# QA Defect Report -- Supply Chain Risk Monitor

Updated: 2026-10-16 (rev 5 -- FINAL) | Source: `streamlit_app.py` (830 lines)
Runtime: Snowflake SiS (older Streamlit -- st.experimental_rerun required, st.rerun NOT available)
Deployed: Live, 5 tabs, matches local file

---

## ALL P0 ISSUES RESOLVED

- ~~P0 STALE DEPLOY~~ -- RESOLVED. App recreated, 5 tabs live.
- ~~P0 Indentation bug (st.experimental_rerun at column 0)~~ -- FIXED. Line 570 now at 12-space indent inside `if st.button("Clear All Filters")` block.
- ~~P0 st.rerun() not available in SiS~~ -- FIXED. Both calls use `st.experimental_rerun()` which works in this Snowflake runtime. Line 340 (View in Explorer) and line 570 (Clear All Filters).
- ~~P0 HEADER inside FILE_FORMAT~~ -- FIXED. `HEADER = TRUE` moved to top-level COPY INTO option (line 724).

---

## ALL PREVIOUSLY REPORTED BUGS -- RESOLVED

| # | Original Issue | Status | Fix Applied |
|---|---|---|---|
| 1 | st.bar_chart color= TypeError | FIXED | Replaced with st.vega_lite_chart (lines 291-319) |
| 2 | st.download_button S3 SignatureDoesNotMatch | FIXED | Replaced with COPY INTO stage + Show SQL |
| 3 | Clear Filters session state conflict | FIXED | Removed default= args, session state only |
| 4 | Slider returns float not tuple | FIXED | Explicit `(0.0, 100.0)` value param (line 605) |
| 5 | No error handling on data load | FIXED | try/except + st.spinner (lines 227-239) |
| 6 | No empty state handling | FIXED | st.stop() for empty supplier data (line 239) and empty detail data (line 575) |
| 7 | No empty filter results handling | FIXED | Warning message when filters return zero rows (line 657) |
| 8 | SQL injection in text search | FIXED | Single-quote escaping (lines 696-700) |
| 9 | st.experimental_rerun indentation | FIXED | Properly indented at 12 spaces (line 570) |
| 10 | st.rerun crashes in SiS | FIXED | Reverted to st.experimental_rerun (lines 340, 570) |
| 11 | HEADER = TRUE in FILE_FORMAT | FIXED | Moved to top-level COPY INTO option (line 724) |
| 12 | Chart names truncated | FIXED | labelAngle: -45, labelLimit: 120 in Vega-Lite |
| 13 | No loading spinner | FIXED | st.spinner wrapping data load (line 228) |
| 14 | Bake score outdated | FIXED | Updated to "4 (Usable by Others)" in footer (line 800) |

---

## REMAINING -- P1/P2 (Non-blocking)

### P1: SQL string concatenation in multiselect filters (lines 666-700)

Multiselect dropdown values from the database are concatenated into SQL without escaping. These values come from Snowflake columns so they're unlikely to contain quotes, but not guaranteed. Text search fields are escaped. Low practical risk for hackathon scope.

### P1: AI model deprecation risk (line 166)

`AI_COMPLETE('llama3.1-8b', ?)` works as of this session. If the model is deprecated, the try/except fallback (line 170-171) shows a user-friendly message. No app crash.

### P2: KPI tooltips are hover-only (lines 54-59)

CSS hover reveal. Does not work on touch devices or screen readers. Non-blocking.

### P2: Top-N selector empty middle column (line 324)

`st.columns([2, 3, 1])` -- the middle column is unused. Cosmetic waste of space.

### P2: Cross-tab navigation requires manual tab click

"View in Explorer" sets filter state and shows an animated banner, but Streamlit cannot switch tabs programmatically. Users must click the DATA EXPLORER tab manually. This is a Streamlit platform limitation, not a bug.

### P3: Footer references hackathon scoring

Line 800: "How Baked Is It? Score: 4 (Usable by Others)" -- appropriate for judges, remove for post-hackathon use.

---

## VERIFIED WORKING (live on Snowflake)

- Executive Overview: 5 KPI cards with hover tooltips (33 Critical, 294 Warning, 73 Healthy)
- Executive Overview: 2 Vega-Lite charts with theme-aware colors and transparent backgrounds
- Executive Overview: Top-N selector (Top 1/5/10/100/All) with dynamic KPIs and supplier table
- Executive Overview: "View in Explorer" button with animated navigation banner
- Manager Dashboard: Supplier Scorecard table with 3 filters + conditional formatting
- Manager Dashboard: AT-RISK PURCHASE ORDERS table with exposure color coding
- Supplier Deep Dive: Supplier dropdown, risk badge, 8 KPI cards, AI summary button
- Supplier Deep Dive: AI_COMPLETE generates real summaries (llama3.1-8b confirmed)
- Data Explorer: 12 filters in 3 rows, Clear All Filters button (properly indented rerun)
- Data Explorer: Export to Stage (COPY INTO with HEADER = TRUE) -- VERIFIED WORKING
- Data Explorer: Show SQL Query button
- Data Explorer: Results summary (row count, supplier count, exposure total)
- Data Explorer: Empty filter results show warning message
- Alerts and System: MONITORING ACTIVE message, Pipeline Architecture table (7 features)
- Theme toggle: Sun/moon icon in header, smooth CSS transitions
- Error handling: Loading spinner on data fetch, empty state checks, graceful AI fallback
- Footer: Bake score 4, hackathon branding
- 5 tabs all visible and functional in deployed app

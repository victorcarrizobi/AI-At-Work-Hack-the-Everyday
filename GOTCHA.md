# Supply Chain Monitor -- Gotcha File

> **Purpose:** Document mistakes, dead ends, and workarounds encountered during this project so future AI sessions (and humans) don't repeat them. Read this before making changes.

---

## GOTCHA-001: Dynamic Tables cannot use secondary roles

- **Session:** CoCo-Session-1 (2026-10-16)
- **What happened:** Created a Dynamic Table referencing `AUTO_MFG_DW` tables. It compiled fine but failed on initial refresh with: `Database 'AUTO_MFG_DW' does not exist or not authorized. Your primary role ATTENDEE_ROLE must have USAGE...`
- **Root cause:** Interactive queries succeed because `CURRENT_SECONDARY_ROLES()` includes ACCOUNTADMIN. But Dynamic Tables (and Tasks, Alerts, Stored Procedures) run as the **owner role only** -- secondary roles are not applied. ATTENDEE_ROLE had no direct grants on AUTO_MFG_DW.
- **Fix:** Explicitly grant access to the owner role:
  ```sql
  GRANT USAGE ON DATABASE AUTO_MFG_DW TO ROLE ATTENDEE_ROLE;
  GRANT USAGE ON ALL SCHEMAS IN DATABASE AUTO_MFG_DW TO ROLE ATTENDEE_ROLE;
  GRANT SELECT ON ALL TABLES IN DATABASE AUTO_MFG_DW TO ROLE ATTENDEE_ROLE;
  ```
- **Rule:** Before creating any Dynamic Table, Task, Alert, or Stored Procedure that references a database, verify the owner role has direct grants. Do not rely on secondary roles.

---

## GOTCHA-002: DMF auto-attach fails with "Function does not exist or not authorized"

- **Session:** CoCo-Session-1 (2026-10-16)
- **What happened:** Created a custom Data Metric Function `UNMANAGED_RISK_COUNT`. It exists (`SHOW USER FUNCTIONS` confirms it, `DESC FUNCTION` works). But `ALTER TABLE ... ADD DATA METRIC FUNCTION ...` fails every time with "Function does not exist or not authorized."
- **Tried and failed:**
  1. Granting OWNERSHIP on the function to ATTENDEE_ROLE
  2. Granting EXECUTE DATA METRIC FUNCTION ON ACCOUNT to ATTENDEE_ROLE
  3. Recreating the DMF with matching column names
  4. Multiple variations of the ALTER TABLE syntax
- **Root cause (suspected):** Trial account edition limitation or specific permission gap that standard grants don't cover. DMFs require Enterprise Edition per docs, and while the CREATE succeeds, the ALTER TABLE attachment may have additional edition gating.
- **Workaround:** The DMF logic is embedded directly in the Streamlit app as a regular SQL query. The DMF object exists for demo purposes and can be called manually.
- **Rule:** Do not spend time debugging DMF attachment on this account. Use the workaround.

---

## GOTCHA-003: AI_COMPLETE model deprecation

- **Session:** CoCo-Session-1 (2026-10-16)
- **What happened:** Tried several models for AI_COMPLETE:
  - `snowflake-llama-3.3-70b` -- deprecated July 8, 2026
  - `llama4-maverick` -- legacy state
  - `claude-3-5-sonnet` -- unknown model
  - `snowflake-arctic` -- unknown model
- **What works:** `llama3.1-8b` -- confirmed working.
- **Rule:** Use `llama3.1-8b` for AI_COMPLETE calls on this account. Do not try other models without testing first.

---

## GOTCHA-004: PARTS_CATALOG.PRIMARY_SUPPLIER_ID is a company code, not a supplier ID

- **Session:** CoCo-Session-1 (2026-10-16)
- **What happened:** Initially tried to join WARRANTY_CLAIMS -> PARTS_CATALOG -> SUPPLIERS using PRIMARY_SUPPLIER_ID. But PRIMARY_SUPPLIER_ID values are company codes like `AM07`, `AM09` -- not supplier IDs (which are integers 1-400).
- **Fix:** Join warranty claims to suppliers through PURCHASE_ORDERS: `WARRANTY_CLAIMS.PART_ID -> PURCHASE_ORDERS.PART_ID -> PURCHASE_ORDERS.SUPPLIER_ID -> SUPPLIERS.SUPPLIER_ID`. Since a part can have multiple suppliers across POs, use the most frequent supplier per part (ROW_NUMBER with QUALIFY).
- **Rule:** Always check column values before assuming join keys match. PRIMARY_SUPPLIER_ID in PARTS_CATALOG refers to the manufacturing company, not the supply chain supplier.

---

## GOTCHA-005: pandas applymap is deprecated

- **Session:** CoCo-Session-1 (2026-10-16)
- **What happened:** Used `df.style.applymap()` in Streamlit app. This is deprecated in newer pandas versions (which SiS may run).
- **Fix:** Use `df.style.map()` instead -- it's the direct replacement.
- **Rule:** Use `style.map()` not `style.applymap()` for element-wise styling in Streamlit apps.

---

## GOTCHA-006: Streamlit stage must exist before CREATE STREAMLIT

- **Session:** CoCo-Session-1 (2026-10-16)
- **What happened:** `CREATE STREAMLIT` failed with "The specified stage STREAMLIT_STAGE does not exist."
- **Fix:** Create the stage first, upload the file, then create the Streamlit object:
  ```sql
  CREATE OR REPLACE STAGE DEFAULT_DATABASE.PUBLIC.STREAMLIT_STAGE;
  PUT 'file://D:/HACKATHON/streamlit_app.py' @DEFAULT_DATABASE.PUBLIC.STREAMLIT_STAGE/ AUTO_COMPRESS=FALSE OVERWRITE=TRUE;
  CREATE OR REPLACE STREAMLIT DEFAULT_DATABASE.PUBLIC.SUPPLY_CHAIN_MONITOR ...;
  ```
- **Rule:** Always create the stage before creating the Streamlit object. Use `AUTO_COMPRESS=FALSE` for .py files.

---

## GOTCHA-007: Dynamic Table FULL refresh mode with CURRENT_TIMESTAMP()

- **Session:** CoCo-Session-1 (2026-10-16)
- **What happened:** SUPPLIER_QUALITY_SCORE DT was created with `CURRENT_TIMESTAMP()` in the SELECT (for LAST_REFRESHED column). Snowflake forced FULL refresh mode instead of incremental.
- **Impact:** Every refresh re-runs AI_CLASSIFY on 8,000 rows and SENTIMENT on 30,000 rows. This is expensive. With a 1-hour TARGET_LAG it's manageable for the hackathon but not for production.
- **Rule:** Avoid non-deterministic functions in Dynamic Tables if incremental refresh is needed. Move CURRENT_TIMESTAMP() to a downstream view or Task if incremental refresh matters.

---

## Quick Reference: What Works on This Account

| Feature | Status | Notes |
|---|---|---|
| Dynamic Tables | Works | Full refresh only (due to CURRENT_TIMESTAMP) |
| AI_CLASSIFY | Works | Used on defect descriptions |
| SENTIMENT | Works | Used on warranty verbatims |
| AI_COMPLETE | Works | Model: `llama3.1-8b` only |
| Alerts | Works | 60-minute schedule, RESUMED |
| Tasks | Works | CRON schedule, RESUMED |
| DMF (create) | Works | Function callable manually |
| DMF (auto-attach) | FAILS | See GOTCHA-002 |
| Streamlit (SiS) | Works | Via stage upload + CREATE STREAMLIT |
| Grants | Works | ATTENDEE_ROLE has MANAGE GRANTS |

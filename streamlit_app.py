import streamlit as st
import pandas as pd
from snowflake.snowpark.context import get_active_session

st.set_page_config(page_title="Supply Chain Risk Monitor", page_icon="\u2699\ufe0f", layout="wide")

# --- Theme Toggle ---
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

def toggle_theme():
    st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"

is_dark = st.session_state.theme == "dark"

# --- Theme Variables ---
if is_dark:
    BG = "#0F172A"; CARD_BG = "#1E293B"; CARD_BG2 = "#1B2336"
    FG = "#F8FAFC"; MUTED = "#94A3B8"; BORDER = "#475569"; BORDER_LIGHT = "#334155"
    ACCENT = "#22C55E"; ACCENT_BG = "#14532D"
    CRIT_BG = "#7F1D1D"; CRIT_FG = "#FCA5A5"
    WARN_BG = "#78350F"; WARN_FG = "#FDE68A"
    HEALTH_BG = "#14532D"; HEALTH_FG = "#86EFAC"
    INFO_COLOR = "#38BDF8"; EXPO_COLOR = "#A78BFA"
    TAB_BG = "#1E293B"; TAB_SEL_BG = "#22C55E"; TAB_SEL_FG = "#0F172A"
    TABLE_HEADER = "#334155"
else:
    BG = "#EFF2F7"; CARD_BG = "#FFFFFF"; CARD_BG2 = "#F1F5F9"
    FG = "#1E293B"; MUTED = "#475569"; BORDER = "#CBD5E1"; BORDER_LIGHT = "#E2E8F0"
    ACCENT = "#16A34A"; ACCENT_BG = "#DCFCE7"
    CRIT_BG = "#FEE2E2"; CRIT_FG = "#B91C1C"
    WARN_BG = "#FEF3C7"; WARN_FG = "#B45309"
    HEALTH_BG = "#DCFCE7"; HEALTH_FG = "#15803D"
    INFO_COLOR = "#0369A1"; EXPO_COLOR = "#6D28D9"
    TAB_BG = "#F1F5F9"; TAB_SEL_BG = "#16A34A"; TAB_SEL_FG = "#FFFFFF"
    TABLE_HEADER = "#E2E8F0"

st.markdown(f"""
<style>
    /* Smooth theme transition */
    .stApp, .stApp * {{ transition: background-color 0.3s ease, color 0.2s ease, border-color 0.3s ease; }}
    .stApp {{ background-color: {BG}; }}
    section[data-testid="stSidebar"] {{ background-color: {CARD_BG2}; }}
    .kpi-card {{
        background: linear-gradient(135deg, {CARD_BG} 0%, {CARD_BG2} 100%);
        border: 1px solid {BORDER};
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        {"box-shadow: 0 1px 3px rgba(0,0,0,0.08), 0 1px 2px rgba(0,0,0,0.06);" if not is_dark else ""}
    }}
    .kpi-value {{ font-size: 2.2rem; font-weight: 700; margin: 4px 0; }}
    .kpi-label {{ font-size: 0.85rem; color: {MUTED}; text-transform: uppercase; letter-spacing: 1px; }}
    .kpi-tip {{
        font-size: 0.7rem; color: {MUTED}; margin-top: 6px; line-height: 1.4;
        max-height: 0; overflow: hidden; opacity: 0;
        transition: max-height 0.3s ease, opacity 0.3s ease;
    }}
    .kpi-card:hover .kpi-tip {{ max-height: 80px; opacity: 1; }}
    .kpi-critical {{ color: {CRIT_FG}; }}
    .kpi-warning {{ color: {WARN_FG}; }}
    .kpi-healthy {{ color: {HEALTH_FG}; }}
    .kpi-info {{ color: {INFO_COLOR}; }}
    .kpi-exposure {{ color: {EXPO_COLOR}; }}
    .risk-badge {{ display: inline-block; padding: 2px 10px; border-radius: 20px; font-size: 0.75rem; font-weight: 600; letter-spacing: 0.5px; }}
    .badge-critical {{ background: {CRIT_BG}; color: {CRIT_FG}; border: 1px solid {CRIT_FG}; }}
    .badge-warning {{ background: {WARN_BG}; color: {WARN_FG}; border: 1px solid {WARN_FG}; }}
    .badge-healthy {{ background: {HEALTH_BG}; color: {HEALTH_FG}; border: 1px solid {HEALTH_FG}; }}
    .section-header {{
        font-size: 1.1rem; font-weight: 600; color: {FG};
        padding: 8px 0; border-bottom: 2px solid {ACCENT}; margin-bottom: 16px;
    }}
    .ai-card {{
        background: {"linear-gradient(135deg, " + CARD_BG + ", " + CARD_BG2 + ")" if not is_dark else "linear-gradient(135deg, " + CARD_BG + ", " + BG + ")"};
        border: 1px solid {INFO_COLOR}; border-radius: 12px;
        padding: 20px; margin: 12px 0; color: {FG};
        {"box-shadow: 0 2px 6px rgba(0,0,0,0.06);" if not is_dark else ""}
    }}
    .ai-card-header {{ color: {INFO_COLOR}; font-weight: 600; font-size: 0.9rem; margin-bottom: 8px; letter-spacing: 0.5px; }}
    .app-header {{
        background: linear-gradient(90deg, {BG} 0%, {CARD_BG} 50%, {BG} 100%);
        border-bottom: 2px solid {ACCENT};
        padding: 12px 24px; margin: -1rem -1rem 1rem -1rem;
        display: flex; align-items: center; justify-content: space-between;
    }}
    .app-header-left {{ text-align: left; }}
    .app-title {{ font-size: 1.6rem; font-weight: 700; color: {FG}; margin: 0; letter-spacing: 1px; }}
    .app-subtitle {{ font-size: 0.8rem; color: {MUTED}; margin-top: 2px; }}
    .app-badge {{
        display: inline-block; background: {ACCENT_BG}; color: {ACCENT};
        padding: 2px 12px; border-radius: 20px; font-size: 0.7rem;
        font-weight: 600; margin-top: 4px; border: 1px solid {ACCENT}; letter-spacing: 1px;
    }}
    .app-footer {{
        text-align: center; color: {MUTED}; font-size: 0.75rem;
        padding: 24px 0 8px 0; border-top: 1px solid {BORDER_LIGHT}; margin-top: 32px;
    }}
    .stTabs [data-baseweb="tab-list"] {{ gap: 8px; }}
    .stTabs [data-baseweb="tab"] {{
        background-color: {TAB_BG}; border-radius: 8px 8px 0 0;
        border: 1px solid {BORDER_LIGHT}; color: {MUTED}; padding: 8px 20px;
    }}
    .stTabs [aria-selected="true"] {{
        background-color: {TAB_SEL_BG} !important; color: {TAB_SEL_FG} !important; font-weight: 600;
    }}
    .filter-row {{ margin-bottom: 8px; }}
    /* Widget overrides for light theme */
    {"" if is_dark else '''
    .stMultiSelect [data-baseweb="select"],
    .stMultiSelect [data-baseweb="popover"],
    .stTextInput input,
    .stNumberInput input,
    .stSelectbox [data-baseweb="select"] {
        background-color: #FFFFFF !important;
        color: #1E293B !important;
        border-color: #CBD5E1 !important;
    }
    .stMultiSelect [data-baseweb="tag"] {
        background-color: #E2E8F0 !important;
        color: #1E293B !important;
    }
    .stMultiSelect label, .stTextInput label, .stNumberInput label,
    .stSelectbox label, .stSlider label {
        color: #1E293B !important;
    }
    [data-baseweb="select"] svg {
        fill: #475569 !important;
    }
    '''}
</style>
""", unsafe_allow_html=True)

session = get_active_session()


@st.cache_data(ttl=300)
def get_supplier_scores():
    return session.sql("SELECT * FROM DEFAULT_DATABASE.PUBLIC.SUPPLIER_QUALITY_SCORE ORDER BY COMPOSITE_RISK_SCORE DESC").to_pandas()


@st.cache_data(ttl=300)
def get_at_risk_pos():
    return session.sql("SELECT * FROM DEFAULT_DATABASE.PUBLIC.AT_RISK_PURCHASE_ORDERS ORDER BY DOLLAR_EXPOSURE DESC LIMIT 500").to_pandas()


@st.cache_data(ttl=300)
def get_at_risk_po_summary():
    return session.sql("""
        SELECT COUNT(*) AS total_count, COALESCE(SUM(DOLLAR_EXPOSURE), 0) AS total_exposure,
               COUNT(CASE WHEN RISK_LEVEL = 'CRITICAL' THEN 1 END) AS critical_count,
               COALESCE(SUM(CASE WHEN RISK_LEVEL = 'CRITICAL' THEN DOLLAR_EXPOSURE END), 0) AS critical_exposure
        FROM DEFAULT_DATABASE.PUBLIC.AT_RISK_PURCHASE_ORDERS
    """).to_pandas()


@st.cache_data(ttl=300)
def get_alert_history():
    return session.sql("SELECT * FROM DEFAULT_DATABASE.PUBLIC.ALERT_HISTORY ORDER BY ALERT_TIMESTAMP DESC LIMIT 50").to_pandas()


@st.cache_data(ttl=300)
def get_detail_data():
    return session.sql("""
        SELECT
            po.PO_NUMBER, po.SUPPLIER_NAME, po.SUPPLIER_TIER, sq.CURRENT_STATUS AS SUPPLIER_STATUS,
            sq.COUNTRY_CODE, po.RISK_LEVEL, sq.COMPOSITE_RISK_SCORE, sq.AI_RISK_SCORE,
            po.PART_NAME, po.PART_CATEGORY,
            sq.TOTAL_DEFECTS, sq.SAFETY_CRITICAL_DEFECTS, sq.WARRANTY_CLAIMS,
            sq.AVG_CUSTOMER_SENTIMENT, sq.BASELINE_QUALITY_RATING, sq.ON_TIME_DELIVERY_PCT,
            po.DOLLAR_EXPOSURE, po.QUANTITY_ORDERED, po.PO_STATUS, po.ORDER_DATE, po.EXPECTED_DELIVERY,
            po.SHIPPING_MODE, po.DESTINATION_PLANT
        FROM DEFAULT_DATABASE.PUBLIC.AT_RISK_PURCHASE_ORDERS po
        JOIN DEFAULT_DATABASE.PUBLIC.SUPPLIER_QUALITY_SCORE sq ON po.SUPPLIER_ID = sq.SUPPLIER_ID
        ORDER BY po.DOLLAR_EXPOSURE DESC
        LIMIT 2000
    """).to_pandas()


def get_ai_summary(supplier_name, risk_score, defects, sentiment, tier):
    prompt = f"""You are a supply chain risk analyst. Summarize this supplier's risk profile in 2-3 sentences.
Supplier: {supplier_name}
Tier: {tier}
Composite Risk Score: {risk_score}/100
Total Defects: {defects}
Avg Customer Sentiment: {sentiment} (scale -1 to 1, negative = unhappy)
Recommend a specific action."""
    try:
        result = session.sql(
            "SELECT SNOWFLAKE.CORTEX.AI_COMPLETE('llama3.1-8b', ?) AS summary",
            params=[prompt]
        ).collect()
        return result[0]["SUMMARY"]
    except Exception as e:
        return f"AI summary unavailable: {str(e)[:100]}. Review this supplier manually based on the metrics above."


def render_kpi(label, value, css_class="kpi-info", tooltip=""):
    tip_html = f'title="{tooltip}"' if tooltip else ""
    st.markdown(f"""
    <div class="kpi-card" {tip_html}>
        <div class="kpi-label">{label}</div>
        <div class="kpi-value {css_class}">{value}</div>
        {"<div class='kpi-tip'>" + tooltip + "</div>" if tooltip else ""}
    </div>
    """, unsafe_allow_html=True)


def risk_badge(level):
    cls = {"CRITICAL": "badge-critical", "WARNING": "badge-warning", "HEALTHY": "badge-healthy"}.get(level, "badge-healthy")
    return f'<span class="risk-badge {cls}">{level}</span>'


def color_risk(val):
    if val == "CRITICAL":
        return f"background-color: {CRIT_BG}; color: {CRIT_FG}"
    elif val == "WARNING":
        return f"background-color: {WARN_BG}; color: {WARN_FG}"
    return f"background-color: {HEALTH_BG}; color: {HEALTH_FG}"


def color_score(val):
    try:
        v = float(val)
        if v >= 58:
            return f"background-color: {CRIT_BG}; color: {CRIT_FG}"
        elif v >= 38:
            return f"background-color: {WARN_BG}; color: {WARN_FG}"
        return ""
    except (ValueError, TypeError):
        return ""


# --- Header with Theme Toggle ---
hdr_col1, hdr_col2 = st.columns([5, 1])
with hdr_col1:
    st.markdown(f"""
    <div style="padding: 4px 0;">
        <div class="app-title">SUPPLY CHAIN RISK MONITOR</div>
        <div class="app-subtitle">AI-Powered Supplier Quality Scoring | Real-Time Risk Detection</div>
        <span class="app-badge">LIVE - DYNAMIC TABLES + CORTEX AI</span>
    </div>
    """, unsafe_allow_html=True)
with hdr_col2:
    theme_icon = "\u2600\ufe0f" if is_dark else "\U0001f319"
    st.button(theme_icon, on_click=toggle_theme, key="theme_toggle", help="Switch to Light mode" if is_dark else "Switch to Dark mode")

st.markdown(f'<hr style="border: 1px solid {ACCENT}; margin: 0 0 16px 0;">', unsafe_allow_html=True)

# --- Load Data with Error Handling ---
try:
    with st.spinner("Loading supplier risk data..."):
        scores_df = get_supplier_scores()
        risk_pos_df = get_at_risk_pos()
        po_summary = get_at_risk_po_summary()
        alert_df = get_alert_history()
except Exception as e:
    st.error(f"Failed to load data from Snowflake. Please refresh the page. Error: {str(e)[:200]}")
    st.stop()

if scores_df.empty:
    st.warning("No supplier data found. The SUPPLIER_QUALITY_SCORE dynamic table may still be refreshing. Please try again in a few minutes.")
    st.stop()

critical_count = int((scores_df["RISK_LEVEL"] == "CRITICAL").sum())
warning_count = int((scores_df["RISK_LEVEL"] == "WARNING").sum())
healthy_count = int((scores_df["RISK_LEVEL"] == "HEALTHY").sum())
total_exposure = float(po_summary["TOTAL_EXPOSURE"].iloc[0])
total_at_risk_po_count = int(po_summary["TOTAL_COUNT"].iloc[0])
critical_exposure = float(po_summary["CRITICAL_EXPOSURE"].iloc[0])
unmanaged = int(
    ((scores_df["RISK_LEVEL"].isin(["CRITICAL", "WARNING"])) & (~scores_df["CURRENT_STATUS"].isin(["SUSPENDED", "PROBATION"]))).sum()
)
avg_risk = scores_df["COMPOSITE_RISK_SCORE"].mean()
top_risk_supplier = scores_df.iloc[0]["SUPPLIER_NAME"] if len(scores_df) > 0 else "N/A"
top_risk_score = scores_df.iloc[0]["COMPOSITE_RISK_SCORE"] if len(scores_df) > 0 else 0

# --- Tabbed Interface ---
tab_exec, tab_mgr, tab_deep, tab_detail, tab_alerts = st.tabs([
    "EXECUTIVE OVERVIEW",
    "MANAGER DASHBOARD",
    "SUPPLIER DEEP DIVE",
    "DATA EXPLORER",
    "ALERTS & SYSTEM"
])

# =============================================
# TAB 1: EXECUTIVE OVERVIEW
# =============================================
with tab_exec:
    st.markdown('<div class="section-header">KEY RISK INDICATORS</div>', unsafe_allow_html=True)
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        render_kpi("Critical Suppliers", critical_count, "kpi-critical",
                   "Composite risk score >= 58. Score = 30% AI defect classification + 20% defect volume + 20% inverse quality rating + 15% warranty claims + 15% negative sentiment.")
    with c2:
        render_kpi("Warning Suppliers", warning_count, "kpi-warning",
                   "Composite risk score 38-57. Same formula as Critical but below the critical threshold.")
    with c3:
        render_kpi("Healthy Suppliers", healthy_count, "kpi-healthy",
                   "Composite risk score below 38. Low defect count, positive sentiment, and strong quality rating.")
    with c4:
        render_kpi("At-Risk Exposure", f"${total_exposure/1e9:.1f}B", "kpi-exposure",
                   "Sum of (quantity x unit price) for all open POs (PENDING/CONFIRMED/SHIPPED) from WARNING or CRITICAL suppliers.")
    with c5:
        render_kpi("Unmanaged Gap", unmanaged, "kpi-critical",
                   "Suppliers scored WARNING or CRITICAL whose status is still ACTIVE -- not yet moved to PROBATION or SUSPENDED.")

    st.markdown("", unsafe_allow_html=True)
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.markdown('<div class="section-header">RISK DISTRIBUTION BY TIER</div>', unsafe_allow_html=True)
        tier_risk = scores_df.groupby(["SUPPLIER_TIER", "RISK_LEVEL"]).size().reset_index(name="COUNT")
        st.vega_lite_chart(tier_risk, {
            "mark": "bar",
            "encoding": {
                "x": {"field": "SUPPLIER_TIER", "type": "nominal", "title": "Tier", "axis": {"labelColor": FG, "titleColor": FG}},
                "y": {"field": "COUNT", "type": "quantitative", "title": "Count", "axis": {"labelColor": FG, "titleColor": FG}},
                "color": {
                    "field": "RISK_LEVEL", "type": "nominal", "title": "Risk",
                    "scale": {"domain": ["CRITICAL", "WARNING", "HEALTHY"], "range": [CRIT_FG, WARN_FG, HEALTH_FG]},
                    "legend": {"labelColor": FG, "titleColor": FG}
                }
            },
            "config": {"view": {"stroke": "transparent"}, "background": "transparent", "axis": {"gridColor": BORDER_LIGHT}},
            "width": "container", "height": 280
        }, use_container_width=True)

    with chart_col2:
        st.markdown('<div class="section-header">TOP 10 HIGHEST RISK SUPPLIERS</div>', unsafe_allow_html=True)
        top10 = scores_df.head(10)[["SUPPLIER_NAME", "COMPOSITE_RISK_SCORE", "RISK_LEVEL"]]
        st.vega_lite_chart(top10, {
            "mark": "bar",
            "encoding": {
                "y": {"field": "SUPPLIER_NAME", "type": "nominal", "title": None,
                       "sort": {"field": "COMPOSITE_RISK_SCORE", "order": "descending"},
                       "axis": {"labelColor": FG, "labelLimit": 160}},
                "x": {"field": "COMPOSITE_RISK_SCORE", "type": "quantitative", "title": "Risk Score",
                       "axis": {"labelColor": FG, "titleColor": FG}},
                "color": {"field": "RISK_LEVEL", "type": "nominal",
                           "scale": {"domain": ["CRITICAL", "WARNING", "HEALTHY"],
                                     "range": [CRIT_FG, WARN_FG, HEALTH_FG]},
                           "legend": None}
            },
            "config": {"view": {"stroke": "transparent"}, "background": "transparent", "axis": {"gridColor": BORDER_LIGHT}},
            "width": "container", "height": 300
        }, use_container_width=True)

    st.markdown('<div class="section-header">EXPOSURE SUMMARY</div>', unsafe_allow_html=True)

    # Top-N selector
    top_col1, top_col2, top_col3 = st.columns([2, 3, 1])
    with top_col1:
        top_option = st.selectbox("Show highest risk", ["Top 1", "Top 5", "Top 10", "Top 100", "All"], index=1, key="exec_top_n")
    with top_col3:
        detail_clicked = st.button("View in Explorer", key="exec_detail_btn")

    show_all = top_option == "All"
    top_n = len(scores_df) if show_all else int(top_option.split(" ")[1])
    top_label = "All" if show_all else top_option

    if detail_clicked:
        top_names = scores_df.head(top_n)["SUPPLIER_NAME"].tolist() if not show_all else []
        st.session_state["det_risk"] = [] if show_all else ["CRITICAL", "WARNING"]
        st.session_state["det_sup_search"] = ""
        st.session_state["_exec_top_suppliers"] = top_names if not show_all else None
        st.session_state["_show_nav_banner"] = top_label
        st.experimental_rerun()

    nav_label = st.session_state.pop("_show_nav_banner", None)
    if nav_label:
        st.markdown(f"""
        <div style="
            background: linear-gradient(90deg, {ACCENT_BG}, {'#0F2A1A' if is_dark else '#D1FAE5'});
            border: 2px solid {ACCENT};
            border-radius: 12px;
            padding: 16px 24px;
            margin: 12px 0;
            text-align: center;
            animation: pulse-border 1.5s ease-in-out 3;
        ">
            <span style="font-size: 1.1rem; font-weight: 700; color: {ACCENT};">
                Filters applied for {nav_label} suppliers
            </span>
            <br>
            <span style="font-size: 1.4rem; color: {FG};">
                Click the <b>DATA EXPLORER</b> tab above to view the filtered results
            </span>
        </div>
        <style>
            @keyframes pulse-border {{
                0% {{ box-shadow: 0 0 0 0 {'rgba(34,197,94,0.5)' if is_dark else 'rgba(22,163,74,0.4)'}; }}
                50% {{ box-shadow: 0 0 0 8px {'rgba(34,197,94,0)' if is_dark else 'rgba(22,163,74,0)'}; }}
                100% {{ box-shadow: 0 0 0 0 {'rgba(34,197,94,0)' if is_dark else 'rgba(22,163,74,0)'}; }}
            }}
        </style>
        """, unsafe_allow_html=True)

    top_suppliers = scores_df.head(top_n) if not show_all else scores_df
    top_exposure_ids = top_suppliers["SUPPLIER_ID"].tolist()
    top_po_exposure = risk_pos_df[risk_pos_df["SUPPLIER_ID"].isin(top_exposure_ids)]["DOLLAR_EXPOSURE"].sum() if len(risk_pos_df) > 0 else 0
    top_po_count = int(risk_pos_df[risk_pos_df["SUPPLIER_ID"].isin(top_exposure_ids)].shape[0]) if len(risk_pos_df) > 0 else 0

    exp_col1, exp_col2, exp_col3 = st.columns(3)
    with exp_col1:
        render_kpi(f"{top_label} PO Exposure", f"${top_po_exposure/1e9:.1f}B", "kpi-critical",
                   f"Dollar exposure from open POs linked to {top_label} highest-risk suppliers.")
    with exp_col2:
        render_kpi(f"{top_label} At-Risk POs", f"{top_po_count:,}", "kpi-warning",
                   f"Count of open POs from {top_label} highest-risk suppliers.")
    with exp_col3:
        render_kpi(f"{top_label} Avg Score", f"{top_suppliers['COMPOSITE_RISK_SCORE'].mean():.1f}", "kpi-info",
                   f"Mean composite risk score of {top_label} suppliers.")

    top_display = top_suppliers[["SUPPLIER_NAME", "SUPPLIER_TIER", "CURRENT_STATUS", "RISK_LEVEL",
                                 "COMPOSITE_RISK_SCORE", "TOTAL_DEFECTS", "SAFETY_CRITICAL_DEFECTS",
                                 "WARRANTY_CLAIMS", "AVG_CUSTOMER_SENTIMENT"]].reset_index(drop=True)
    st.dataframe(
        top_display.style.map(color_risk, subset=["RISK_LEVEL"]).map(color_score, subset=["COMPOSITE_RISK_SCORE"]),
        use_container_width=True, height=min(200 + len(top_display) * 15, 450)
    )

# =============================================
# TAB 2: MANAGER DASHBOARD
# =============================================
with tab_mgr:
    st.markdown('<div class="section-header">SUPPLIER SCORECARD</div>', unsafe_allow_html=True)
    filter_col1, filter_col2, filter_col3 = st.columns(3)
    with filter_col1:
        tier_filter = st.multiselect("Tier", options=sorted(scores_df["SUPPLIER_TIER"].unique()), default=[], key="mgr_tier")
    with filter_col2:
        risk_filter = st.multiselect("Risk Level", options=["CRITICAL", "WARNING", "HEALTHY"], default=[], key="mgr_risk")
    with filter_col3:
        status_filter = st.multiselect("Status", options=sorted(scores_df["CURRENT_STATUS"].unique()), default=[], key="mgr_status")

    filtered_df = scores_df.copy()
    if tier_filter:
        filtered_df = filtered_df[filtered_df["SUPPLIER_TIER"].isin(tier_filter)]
    if risk_filter:
        filtered_df = filtered_df[filtered_df["RISK_LEVEL"].isin(risk_filter)]
    if status_filter:
        filtered_df = filtered_df[filtered_df["CURRENT_STATUS"].isin(status_filter)]

    display_cols = [
        "SUPPLIER_NAME", "SUPPLIER_TIER", "CURRENT_STATUS", "RISK_LEVEL",
        "COMPOSITE_RISK_SCORE", "AI_RISK_SCORE", "TOTAL_DEFECTS",
        "SAFETY_CRITICAL_DEFECTS", "WARRANTY_CLAIMS", "AVG_CUSTOMER_SENTIMENT",
        "BASELINE_QUALITY_RATING", "ON_TIME_DELIVERY_PCT"
    ]

    styled = filtered_df[display_cols].style.map(
        color_risk, subset=["RISK_LEVEL"]
    ).map(
        color_score, subset=["COMPOSITE_RISK_SCORE"]
    )
    st.dataframe(styled, use_container_width=True, height=450)

    st.markdown('<div class="section-header">AT-RISK PURCHASE ORDERS</div>', unsafe_allow_html=True)
    po_col1, po_col2 = st.columns(2)
    with po_col1:
        po_risk_filter = st.selectbox("Filter by Risk", ["ALL", "CRITICAL", "WARNING"], key="mgr_po_risk")
    with po_col2:
        po_sort = st.selectbox("Sort By", ["DOLLAR_EXPOSURE", "COMPOSITE_RISK_SCORE", "EXPECTED_DELIVERY"], key="mgr_po_sort")

    po_display = risk_pos_df.copy()
    if po_risk_filter != "ALL":
        po_display = po_display[po_display["RISK_LEVEL"] == po_risk_filter]
    po_display = po_display.sort_values(po_sort, ascending=False)

    po_cols = [
        "PO_NUMBER", "SUPPLIER_NAME", "SUPPLIER_TIER", "RISK_LEVEL",
        "COMPOSITE_RISK_SCORE", "PART_NAME", "PART_CATEGORY",
        "DOLLAR_EXPOSURE", "PO_STATUS", "EXPECTED_DELIVERY", "DESTINATION_PLANT"
    ]

    def color_exposure(val):
        try:
            v = float(val)
            if v > 10_000_000:
                return f"color: {CRIT_FG}; font-weight: 600"
            elif v > 1_000_000:
                return f"color: {WARN_FG}"
            return ""
        except (ValueError, TypeError):
            return ""

    po_styled = po_display[po_cols].head(100).style.map(
        color_risk, subset=["RISK_LEVEL"]
    ).map(
        color_exposure, subset=["DOLLAR_EXPOSURE"]
    )
    st.dataframe(po_styled, use_container_width=True, height=400)

# =============================================
# TAB 3: SUPPLIER DEEP DIVE
# =============================================
with tab_deep:
    st.markdown('<div class="section-header">SUPPLIER INVESTIGATION</div>', unsafe_allow_html=True)
    supplier_names = sorted(scores_df["SUPPLIER_NAME"].unique())
    selected_supplier = st.selectbox("Select a Supplier to Investigate", supplier_names, key="deep_supplier")

    if selected_supplier:
        supplier_row = scores_df[scores_df["SUPPLIER_NAME"] == selected_supplier].iloc[0]
        risk_level = supplier_row["RISK_LEVEL"]

        st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 16px;">
            <span style="font-size: 1.4rem; font-weight: 700; color: {FG};">{selected_supplier}</span>
            {risk_badge(risk_level)}
            <span style="color: {MUTED};">| {supplier_row['SUPPLIER_TIER']} | {supplier_row['COUNTRY_CODE']}</span>
        </div>
        """, unsafe_allow_html=True)

        d1, d2, d3, d4 = st.columns(4)
        with d1:
            render_kpi("Risk Score", f"{supplier_row['COMPOSITE_RISK_SCORE']:.1f}",
                       "kpi-critical" if risk_level == "CRITICAL" else "kpi-warning" if risk_level == "WARNING" else "kpi-healthy",
                       "Weighted composite: 30% AI-classified defect risk + 20% defect volume + 20% inverse quality rating + 15% warranty volume + 15% negative sentiment.")
        with d2:
            render_kpi("AI Risk Score", f"{supplier_row['AI_RISK_SCORE']:.1f}", "kpi-info",
                       "Average risk from AI_CLASSIFY on defect text. SAFETY_CRITICAL=100, PERFORMANCE=70, COSMETIC=30, WEAR_AND_TEAR=15.")
        with d3:
            render_kpi("Total Defects", int(supplier_row["TOTAL_DEFECTS"]),
                       "kpi-critical" if supplier_row["TOTAL_DEFECTS"] > 40 else "kpi-warning",
                       "Count of all defect records in AUTO_MFG_DW.QUALITY.DEFECTS linked to this supplier.")
        with d4:
            render_kpi("Warranty Claims", int(supplier_row["WARRANTY_CLAIMS"]),
                       "kpi-critical" if supplier_row["WARRANTY_CLAIMS"] > 100 else "kpi-info",
                       "Count of warranty claims on parts supplied by this supplier, joined via purchase orders.")

        st.markdown("", unsafe_allow_html=True)
        d5, d6, d7, d8 = st.columns(4)
        with d5:
            render_kpi("Safety-Critical", int(supplier_row["SAFETY_CRITICAL_DEFECTS"]), "kpi-critical",
                       "Defects where AI_CLASSIFY labeled the description as SAFETY_CRITICAL.")
        with d6:
            sent = supplier_row["AVG_CUSTOMER_SENTIMENT"]
            render_kpi("Avg Sentiment", f"{sent:.3f}",
                       "kpi-critical" if sent < -0.3 else "kpi-warning" if sent < 0 else "kpi-healthy",
                       "Average SNOWFLAKE.CORTEX.SENTIMENT() score on warranty customer verbatim text. Range -1 (very negative) to +1 (very positive).")
        with d7:
            render_kpi("On-Time Delivery", f"{supplier_row['ON_TIME_DELIVERY_PCT']:.1f}%", "kpi-info",
                       "Supplier's on-time delivery percentage from the supplier master record.")
        with d8:
            render_kpi("Quality Rating", f"{supplier_row['BASELINE_QUALITY_RATING']:.1f}", "kpi-info",
                       "Baseline quality rating from the supplier master record (0-100 scale).")

        st.markdown("", unsafe_allow_html=True)
        if st.button("Generate AI Risk Summary", key="deep_ai_btn"):
            with st.spinner("Cortex AI analyzing supplier risk profile..."):
                summary = get_ai_summary(
                    supplier_row["SUPPLIER_NAME"],
                    supplier_row["COMPOSITE_RISK_SCORE"],
                    supplier_row["TOTAL_DEFECTS"],
                    supplier_row["AVG_CUSTOMER_SENTIMENT"],
                    supplier_row["SUPPLIER_TIER"],
                )
                st.markdown(f"""
                <div class="ai-card">
                    <div class="ai-card-header">CORTEX AI RISK ASSESSMENT</div>
                    {summary}
                </div>
                """, unsafe_allow_html=True)

        supplier_pos = risk_pos_df[risk_pos_df["SUPPLIER_NAME"] == selected_supplier]
        if len(supplier_pos) > 0:
            st.markdown(f'<div class="section-header">AT-RISK POs ({len(supplier_pos)})</div>', unsafe_allow_html=True)
            st.dataframe(
                supplier_pos[["PO_NUMBER", "PART_NAME", "PART_CATEGORY", "DOLLAR_EXPOSURE", "PO_STATUS", "EXPECTED_DELIVERY", "DESTINATION_PLANT"]],
                use_container_width=True, height=300
            )
        else:
            st.success("No at-risk purchase orders for this supplier.")

# =============================================
# TAB 4: DATA EXPLORER
# =============================================
with tab_detail:
    st.markdown('<div class="section-header">COMBINED DATA EXPLORER</div>', unsafe_allow_html=True)

    # Check if navigated from Executive with pre-filtered suppliers
    _exec_suppliers = st.session_state.pop("_exec_top_suppliers", None)
    if _exec_suppliers:
        st.success(f"Showing data for top {len(_exec_suppliers)} highest-risk suppliers. Use Clear All Filters to reset.")

    hdr1, hdr2 = st.columns([4, 1])
    with hdr1:
        st.caption("Filter across suppliers and purchase orders. Results are exportable as CSV.")
    with hdr2:
        if st.button("Clear All Filters", key="det_clear"):
            for k in ["det_risk", "det_tier", "det_status", "det_cat", "det_po_st",
                       "det_plant", "det_ship", "det_country"]:
                st.session_state[k] = []
            st.session_state["det_score"] = (0.0, 100.0)
            st.session_state["det_exp_min"] = 0
            st.session_state["det_sup_search"] = ""
            st.session_state["det_part_search"] = ""
            st.experimental_rerun()

    detail_df = get_detail_data()
    if detail_df.empty:
        st.info("No at-risk purchase order data available. The AT_RISK_PURCHASE_ORDERS dynamic table may still be refreshing.")
        st.stop()

    # Initialize filter defaults in session state (only on first load)
    if "det_score" not in st.session_state:
        st.session_state["det_score"] = (0.0, 100.0)
    if "det_exp_min" not in st.session_state:
        st.session_state["det_exp_min"] = 0

    # --- Row 1: 5 filters ---
    f1, f2, f3, f4, f5 = st.columns(5)
    with f1:
        det_risk = st.multiselect("Risk Level", options=sorted(detail_df["RISK_LEVEL"].unique()), key="det_risk")
    with f2:
        det_tier = st.multiselect("Supplier Tier", options=sorted(detail_df["SUPPLIER_TIER"].unique()), key="det_tier")
    with f3:
        det_status = st.multiselect("Supplier Status", options=sorted(detail_df["SUPPLIER_STATUS"].unique()), key="det_status")
    with f4:
        det_category = st.multiselect("Part Category", options=sorted(detail_df["PART_CATEGORY"].unique()), key="det_cat")
    with f5:
        det_po_status = st.multiselect("PO Status", options=sorted(detail_df["PO_STATUS"].unique()), key="det_po_st")

    # --- Row 2: 5 more filters ---
    f6, f7, f8, f9, f10 = st.columns(5)
    with f6:
        det_plant = st.multiselect("Destination Plant", options=sorted(detail_df["DESTINATION_PLANT"].dropna().unique()), key="det_plant")
    with f7:
        det_ship = st.multiselect("Shipping Mode", options=sorted(detail_df["SHIPPING_MODE"].dropna().unique()), key="det_ship")
    with f8:
        det_country = st.multiselect("Country", options=sorted(detail_df["COUNTRY_CODE"].unique()), key="det_country")
    with f9:
        score_range = st.slider("Risk Score Range", 0.0, 100.0, (0.0, 100.0), key="det_score")
    with f10:
        exposure_min = st.number_input("Min Exposure ($)", min_value=0, step=100000, key="det_exp_min")

    # --- Row 3: text search + part name ---
    f11, f12 = st.columns(2)
    with f11:
        supplier_search = st.text_input("Search Supplier Name", key="det_sup_search")
    with f12:
        part_search = st.text_input("Search Part Name", key="det_part_search")

    # Apply all filters
    df = detail_df.copy()
    if _exec_suppliers:
        df = df[df["SUPPLIER_NAME"].isin(_exec_suppliers)]
    if det_risk:
        df = df[df["RISK_LEVEL"].isin(det_risk)]
    if det_tier:
        df = df[df["SUPPLIER_TIER"].isin(det_tier)]
    if det_status:
        df = df[df["SUPPLIER_STATUS"].isin(det_status)]
    if det_category:
        df = df[df["PART_CATEGORY"].isin(det_category)]
    if det_po_status:
        df = df[df["PO_STATUS"].isin(det_po_status)]
    if det_plant:
        df = df[df["DESTINATION_PLANT"].isin(det_plant)]
    if det_ship:
        df = df[df["SHIPPING_MODE"].isin(det_ship)]
    if det_country:
        df = df[df["COUNTRY_CODE"].isin(det_country)]
    df = df[(df["COMPOSITE_RISK_SCORE"] >= score_range[0]) & (df["COMPOSITE_RISK_SCORE"] <= score_range[1])]
    if exposure_min > 0:
        df = df[df["DOLLAR_EXPOSURE"] >= exposure_min]
    if supplier_search:
        df = df[df["SUPPLIER_NAME"].str.contains(supplier_search, case=False, na=False)]
    if part_search:
        df = df[df["PART_NAME"].str.contains(part_search, case=False, na=False)]

    # Results summary
    if df.empty:
        st.warning("No results match the current filters. Try adjusting or clearing filters.")
    else:
        st.markdown(f"""
        <div style="display: flex; gap: 24px; margin: 8px 0 16px 0; color: {FG};">
            <span><b>{len(df):,}</b> rows matched</span>
            <span>|</span>
            <span><b>{df['SUPPLIER_NAME'].nunique()}</b> suppliers</span>
            <span>|</span>
            <span>Exposure: <b>${df['DOLLAR_EXPOSURE'].sum():,.0f}</b></span>
        </div>
        """, unsafe_allow_html=True)

    # Display table
    st.dataframe(
        df.style.map(color_risk, subset=["RISK_LEVEL"]).map(color_score, subset=["COMPOSITE_RISK_SCORE"]),
        use_container_width=True,
        height=500
    )

    # Export section -- build SQL query for all export methods
    where_clauses = []
    if det_risk:
        vals = "', '".join(det_risk)
        where_clauses.append(f"po.RISK_LEVEL IN ('{vals}')")
    if det_tier:
        vals = "', '".join(det_tier)
        where_clauses.append(f"po.SUPPLIER_TIER IN ('{vals}')")
    if det_status:
        vals = "', '".join(det_status)
        where_clauses.append(f"sq.CURRENT_STATUS IN ('{vals}')")
    if det_category:
        vals = "', '".join(det_category)
        where_clauses.append(f"po.PART_CATEGORY IN ('{vals}')")
    if det_po_status:
        vals = "', '".join(det_po_status)
        where_clauses.append(f"po.PO_STATUS IN ('{vals}')")
    if det_plant:
        vals = "', '".join(det_plant)
        where_clauses.append(f"po.DESTINATION_PLANT IN ('{vals}')")
    if det_ship:
        vals = "', '".join(det_ship)
        where_clauses.append(f"po.SHIPPING_MODE IN ('{vals}')")
    if det_country:
        vals = "', '".join(det_country)
        where_clauses.append(f"sq.COUNTRY_CODE IN ('{vals}')")
    if score_range != (0.0, 100.0):
        where_clauses.append(f"sq.COMPOSITE_RISK_SCORE BETWEEN {score_range[0]} AND {score_range[1]}")
    if exposure_min > 0:
        where_clauses.append(f"po.DOLLAR_EXPOSURE >= {exposure_min}")
    if supplier_search:
        safe_sup = supplier_search.replace("'", "''")
        where_clauses.append(f"po.SUPPLIER_NAME ILIKE '%{safe_sup}%'")
    if part_search:
        safe_part = part_search.replace("'", "''")
        where_clauses.append(f"po.PART_NAME ILIKE '%{safe_part}%'")

    where_sql = "\n  AND ".join(where_clauses) if where_clauses else "1=1"

    export_sql = f"""SELECT
    po.PO_NUMBER, po.SUPPLIER_NAME, po.SUPPLIER_TIER,
    sq.CURRENT_STATUS, sq.COUNTRY_CODE, po.RISK_LEVEL,
    sq.COMPOSITE_RISK_SCORE, sq.AI_RISK_SCORE,
    po.PART_NAME, po.PART_CATEGORY,
    sq.TOTAL_DEFECTS, sq.SAFETY_CRITICAL_DEFECTS,
    sq.WARRANTY_CLAIMS, sq.AVG_CUSTOMER_SENTIMENT,
    po.DOLLAR_EXPOSURE, po.PO_STATUS,
    po.ORDER_DATE, po.EXPECTED_DELIVERY,
    po.SHIPPING_MODE, po.DESTINATION_PLANT
FROM DEFAULT_DATABASE.PUBLIC.AT_RISK_PURCHASE_ORDERS po
JOIN DEFAULT_DATABASE.PUBLIC.SUPPLIER_QUALITY_SCORE sq
  ON po.SUPPLIER_ID = sq.SUPPLIER_ID
WHERE {where_sql}
ORDER BY po.DOLLAR_EXPOSURE DESC"""

    exp_col1, exp_col2 = st.columns(2)
    with exp_col1:
        if st.button(f"Export to Stage ({len(df):,} rows)", key="det_export"):
            try:
                copy_sql = f"""COPY INTO @DEFAULT_DATABASE.PUBLIC.STREAMLIT_STAGE/exports/supply_chain_risk_export.csv
FROM ({export_sql})
FILE_FORMAT = (TYPE = CSV COMPRESSION = NONE FIELD_OPTIONALLY_ENCLOSED_BY = '"')
OVERWRITE = TRUE
SINGLE = TRUE
HEADER = TRUE"""
                session.sql(copy_sql).collect()
                st.success("Exported successfully.")
                st.code("-- Download from Snowsight SQL worksheet:\nGET @DEFAULT_DATABASE.PUBLIC.STREAMLIT_STAGE/exports/supply_chain_risk_export.csv file:///tmp/;", language="sql")
            except Exception as e:
                st.warning(f"Stage export failed: {str(e)[:150]}")
                st.info("Copy the SQL query below and run it in a Snowsight SQL worksheet. Use the download button in the results panel.")
    with exp_col2:
        if st.button("Show SQL Query", key="det_show_sql"):
            st.code(export_sql + ";", language="sql")
            st.caption("Copy this query, paste into a Snowsight SQL worksheet, run it, then click the download icon in the results panel.")


# =============================================
# TAB 5: ALERTS & SYSTEM
# =============================================
with tab_alerts:
    st.markdown('<div class="section-header">ALERT HISTORY</div>', unsafe_allow_html=True)
    if len(alert_df) > 0:
        st.dataframe(alert_df, use_container_width=True)
    else:
        st.markdown(f"""
        <div class="ai-card">
            <div class="ai-card-header">MONITORING ACTIVE</div>
            Alert checks every 60 minutes for critical-risk suppliers with non-suspended/non-probation status.
            No alerts have fired yet in this cycle.
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="section-header">PIPELINE ARCHITECTURE</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="ai-card">
        <div class="ai-card-header">SNOWFLAKE FEATURES POWERING THIS MONITOR</div>
        <table style="width:100%; color: {FG}; font-size: 0.85rem;">
            <tr style="border-bottom: 1px solid {BORDER_LIGHT};">
                <td style="padding: 8px; color: {ACCENT}; font-weight: 600;">Dynamic Tables</td>
                <td style="padding: 8px;">SUPPLIER_QUALITY_SCORE and AT_RISK_PURCHASE_ORDERS refresh automatically every hour</td>
            </tr>
            <tr style="border-bottom: 1px solid {BORDER_LIGHT};">
                <td style="padding: 8px; color: {ACCENT}; font-weight: 600;">AI_CLASSIFY</td>
                <td style="padding: 8px;">Categorizes 8,000 defect descriptions into SAFETY_CRITICAL, PERFORMANCE, COSMETIC, WEAR_AND_TEAR</td>
            </tr>
            <tr style="border-bottom: 1px solid {BORDER_LIGHT};">
                <td style="padding: 8px; color: {ACCENT}; font-weight: 600;">SENTIMENT</td>
                <td style="padding: 8px;">Scores 30,000 warranty customer complaint texts for severity</td>
            </tr>
            <tr style="border-bottom: 1px solid {BORDER_LIGHT};">
                <td style="padding: 8px; color: {ACCENT}; font-weight: 600;">AI_COMPLETE</td>
                <td style="padding: 8px;">Generates natural-language risk summaries per supplier on demand</td>
            </tr>
            <tr style="border-bottom: 1px solid {BORDER_LIGHT};">
                <td style="padding: 8px; color: {ACCENT}; font-weight: 600;">Alert</td>
                <td style="padding: 8px;">Fires every 60 minutes when critical-risk suppliers are not suspended or on probation</td>
            </tr>
            <tr style="border-bottom: 1px solid {BORDER_LIGHT};">
                <td style="padding: 8px; color: {ACCENT}; font-weight: 600;">Task</td>
                <td style="padding: 8px;">Daily 6 AM ET snapshots of risk scores for trend tracking</td>
            </tr>
            <tr>
                <td style="padding: 8px; color: {ACCENT}; font-weight: 600;">DMF</td>
                <td style="padding: 8px;">UNMANAGED_RISK_COUNT measures suppliers at risk but not yet actioned</td>
            </tr>
        </table>
    </div>
    """, unsafe_allow_html=True)

# --- Footer ---
st.markdown(f"""
<div class="app-footer">
    DATA IN THE D 2026 HACKATHON | HACK THE GRIND TRACK |
    Powered by Snowflake Dynamic Tables, Cortex AI (AI_CLASSIFY, SENTIMENT, AI_COMPLETE), Alerts, Tasks, and DMFs<br>
    How Baked Is It? Score: 4 (Usable by Others) | Built with CoCo
</div>
""", unsafe_allow_html=True)

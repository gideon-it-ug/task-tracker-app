import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import date, datetime, timedelta
import random

# ─────────────────────────────────────────────
# Page Config & Custom CSS
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="ProductivityOS",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

:root {
    --bg-primary: #0a0a0f;
    --bg-card: #111118;
    --bg-card2: #16161f;
    --accent: #7c3aed;
    --accent2: #06b6d4;
    --accent3: #10b981;
    --warn: #f59e0b;
    --danger: #ef4444;
    --text-primary: #f1f5f9;
    --text-secondary: #94a3b8;
    --border: #1e1e2e;
}

html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif !important;
    background-color: var(--bg-primary) !important;
    color: var(--text-primary) !important;
}

/* Hide Streamlit branding */
#MainMenu, footer, header { visibility: hidden; }

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d0d15 0%, #0a0a12 100%) !important;
    border-right: 1px solid var(--border);
}

section[data-testid="stSidebar"] .stMarkdown h2 {
    color: var(--accent2) !important;
    font-size: 0.75rem !important;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    font-weight: 600;
}

/* Main area */
.main .block-container {
    background-color: var(--bg-primary) !important;
    padding-top: 1.5rem !important;
}

/* Metric cards */
[data-testid="stMetric"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    padding: 1.25rem 1.5rem !important;
    transition: border-color 0.2s ease;
}

[data-testid="stMetric"]:hover {
    border-color: var(--accent) !important;
}

[data-testid="stMetricLabel"] {
    color: var(--text-secondary) !important;
    font-size: 0.75rem !important;
    text-transform: uppercase;
    letter-spacing: 0.1em;
}

[data-testid="stMetricValue"] {
    color: var(--text-primary) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 2rem !important;
    font-weight: 600 !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, var(--accent), #9333ea) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    letter-spacing: 0.03em;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 15px rgba(124, 58, 237, 0.3) !important;
}

.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(124, 58, 237, 0.5) !important;
}

/* Success button (complete task) */
.complete-btn button {
    background: linear-gradient(135deg, var(--accent3), #059669) !important;
    box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3) !important;
}

/* Inputs */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div,
.stDateInput > div > div > input {
    background-color: var(--bg-card2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text-primary) !important;
    font-family: 'Space Grotesk', sans-serif !important;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px rgba(124, 58, 237, 0.2) !important;
}

/* DataFrames */
.stDataFrame {
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    overflow: hidden;
}

/* Plotly charts background */
.js-plotly-plot {
    border-radius: 12px !important;
}

/* Dividers */
hr { border-color: var(--border) !important; }

/* Task card */
.task-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-left: 3px solid var(--accent);
    border-radius: 10px;
    padding: 1rem 1.25rem;
    margin-bottom: 0.75rem;
    transition: border-color 0.2s ease;
}

.task-card:hover { border-left-color: var(--accent2); }
.task-card.completed { border-left-color: var(--accent3); opacity: 0.75; }
.task-card.overdue { border-left-color: var(--danger); }

/* Priority badges */
.badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 999px;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}
.badge-high   { background: rgba(239,68,68,0.15);   color: #f87171; border: 1px solid rgba(239,68,68,0.3); }
.badge-medium { background: rgba(245,158,11,0.15);  color: #fbbf24; border: 1px solid rgba(245,158,11,0.3); }
.badge-low    { background: rgba(16,185,129,0.15);  color: #34d399; border: 1px solid rgba(16,185,129,0.3); }
.badge-done   { background: rgba(6,182,212,0.15);   color: #22d3ee; border: 1px solid rgba(6,182,212,0.3); }

/* Header */
.dashboard-header {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 0.25rem;
}

.header-title {
    font-size: 1.75rem;
    font-weight: 700;
    background: linear-gradient(135deg, #f1f5f9 0%, #7c3aed 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.header-sub {
    color: var(--text-secondary);
    font-size: 0.85rem;
    margin-bottom: 1.5rem;
}

/* Progress bar container */
.progress-wrap {
    background: var(--bg-card2);
    border-radius: 999px;
    height: 6px;
    overflow: hidden;
    margin: 6px 0 2px;
}
.progress-fill {
    height: 100%;
    border-radius: 999px;
    background: linear-gradient(90deg, var(--accent), var(--accent2));
    transition: width 0.4s ease;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# Session State Init
# ─────────────────────────────────────────────
if "tasks" not in st.session_state or not isinstance(st.session_state.tasks, pd.DataFrame):
    # Seed with sample data so dashboard looks alive on first load
    sample_data = [
        {"Title": "Q2 Strategy Report",    "Description": "Draft and finalize quarterly strategy", "Due Date": date.today() + timedelta(days=3),  "Status": "Pending",   "Priority": "High",   "Category": "Management"},
        {"Title": "Client Presentation",   "Description": "Prepare slides for Acme Corp meeting",   "Due Date": date.today() - timedelta(days=1),  "Status": "Pending",   "Priority": "High",   "Category": "Sales"},
        {"Title": "Onboard New Dev",        "Description": "Set up environment and access",          "Due Date": date.today() + timedelta(days=7),  "Status": "Completed", "Priority": "Medium", "Category": "HR"},
        {"Title": "Update Dependencies",   "Description": "Upgrade all npm packages to latest",     "Due Date": date.today() + timedelta(days=5),  "Status": "Pending",   "Priority": "Low",    "Category": "Engineering"},
        {"Title": "Write Unit Tests",       "Description": "Coverage for auth module",               "Due Date": date.today() + timedelta(days=2),  "Status": "Completed", "Priority": "Medium", "Category": "Engineering"},
    ]
    st.session_state.tasks = pd.DataFrame(sample_data)

if "view_mode" not in st.session_state:
    st.session_state.view_mode = "Cards"


# ─────────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚡ ProductivityOS")
    st.markdown("---")
    st.markdown("## ADD TASK")

    with st.form("add_task_form", clear_on_submit=True):
        t_title    = st.text_input("Title", placeholder="e.g. Fix login bug")
        t_desc     = st.text_area("Description", placeholder="Details…", height=80)
        t_due      = st.date_input("Due Date", min_value=date.today())
        t_priority = st.selectbox("Priority", ["High", "Medium", "Low"])
        t_category = st.selectbox("Category", ["Engineering", "Management", "Sales", "HR", "Design", "Other"])
        submitted  = st.form_submit_button("＋ Add Task", use_container_width=True)

    if submitted and t_title.strip():
        new_task = {
            "Title":       t_title.strip(),
            "Description": t_desc.strip(),
            "Due Date":    t_due,
            "Status":      "Pending",
            "Priority":    t_priority,
            "Category":    t_category,
        }
        st.session_state.tasks = pd.concat(
            [st.session_state.tasks, pd.DataFrame([new_task])],
            ignore_index=True
        )
        st.success(f"✅ '{t_title}' added!")
    elif submitted:
        st.warning("Please enter a task title.")

    st.markdown("---")
    st.markdown("## FILTERS")
    filter_status   = st.selectbox("Status",   ["All", "Pending", "Completed"])
    filter_priority = st.selectbox("Priority", ["All", "High", "Medium", "Low"])
    filter_category = st.selectbox("Category", ["All"] + sorted(st.session_state.tasks["Category"].unique().tolist()))

    st.markdown("---")
    st.markdown("## VIEW")
    st.session_state.view_mode = st.radio("Display as", ["Cards", "Table"], horizontal=True)

    st.markdown("---")
    if st.button("🗑️ Clear All Tasks", use_container_width=True):
        st.session_state.tasks = pd.DataFrame(
            columns=["Title","Description","Due Date","Status","Priority","Category"]
        )
        st.rerun()


# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────
def get_priority_badge(p):
    p = str(p).lower()
    if p == "high":   return '<span class="badge badge-high">High</span>'
    if p == "medium": return '<span class="badge badge-medium">Medium</span>'
    return '<span class="badge badge-low">Low</span>'

def is_overdue(row):
    try:
        d = pd.to_datetime(row["Due Date"]).date()
        return row["Status"] == "Pending" and d < date.today()
    except Exception:
        return False


# ─────────────────────────────────────────────
# Computed stats
# ─────────────────────────────────────────────
df = st.session_state.tasks.copy()
df["Due Date"] = pd.to_datetime(df["Due Date"])

total     = len(df)
completed = len(df[df.Status == "Completed"])
pending   = len(df[df.Status == "Pending"])
overdue   = int(df.apply(is_overdue, axis=1).sum())
pct_done  = int((completed / total * 100) if total > 0 else 0)

# Apply filters
filtered = df.copy()
if filter_status   != "All": filtered = filtered[filtered.Status   == filter_status]
if filter_priority != "All": filtered = filtered[filtered.Priority == filter_priority]
if filter_category != "All": filtered = filtered[filtered.Category == filter_category]


# ─────────────────────────────────────────────
# Header
# ─────────────────────────────────────────────
st.markdown(
    '<div class="dashboard-header">'
    '<span style="font-size:2rem">⚡</span>'
    '<span class="header-title">ProductivityOS</span>'
    '</div>'
    f'<p class="header-sub">Welcome back — {date.today().strftime("%A, %B %d %Y")} · '
    f'{pending} tasks pending · {overdue} overdue</p>',
    unsafe_allow_html=True
)


# ─────────────────────────────────────────────
# KPI Metrics
# ─────────────────────────────────────────────
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Total Tasks",     total)
c2.metric("Completed",       completed,  delta=f"+{completed}" if completed else None)
c3.metric("Pending",         pending)
c4.metric("Overdue ⚠️",      overdue,    delta=f"-{overdue}"   if overdue else None,   delta_color="inverse")
c5.metric("Completion Rate", f"{pct_done}%")

# Completion progress bar
st.markdown(
    f'<div style="margin:0.5rem 0 1.5rem">'
    f'<div style="display:flex;justify-content:space-between;font-size:0.75rem;color:#94a3b8;margin-bottom:4px">'
    f'<span>Overall Progress</span><span>{pct_done}%</span></div>'
    f'<div class="progress-wrap"><div class="progress-fill" style="width:{pct_done}%"></div></div>'
    f'</div>',
    unsafe_allow_html=True
)


# ─────────────────────────────────────────────
# Analytics Row
# ─────────────────────────────────────────────
st.markdown("### 📈 Analytics")
col_a, col_b, col_c = st.columns(3)

chart_theme = {
    "paper_bgcolor": "rgba(0,0,0,0)",
    "plot_bgcolor":  "rgba(0,0,0,0)",
    "font":          {"family": "Space Grotesk", "color": "#94a3b8"},
}

with col_a:
    if total > 0:
        status_counts = df.groupby("Status").size().reset_index(name="count")
        fig1 = px.pie(
            status_counts, names="Status", values="count",
            title="Status Breakdown",
            color="Status",
            color_discrete_map={"Completed": "#10b981", "Pending": "#7c3aed"},
            hole=0.55
        )
        fig1.update_layout(**chart_theme, title_font_color="#f1f5f9",
                           legend_font_color="#94a3b8", margin=dict(t=40,b=10,l=10,r=10))
        fig1.update_traces(textfont_color="white")
        st.plotly_chart(fig1, use_container_width=True)

with col_b:
    if total > 0:
        pri_counts = df.groupby("Priority").size().reset_index(name="count")
        pri_order  = {"High": 0, "Medium": 1, "Low": 2}
        pri_counts["order"] = pri_counts["Priority"].map(pri_order)
        pri_counts = pri_counts.sort_values("order")
        fig2 = px.bar(
            pri_counts, x="Priority", y="count",
            title="Tasks by Priority",
            color="Priority",
            color_discrete_map={"High": "#ef4444", "Medium": "#f59e0b", "Low": "#10b981"}
        )
        fig2.update_layout(**chart_theme, title_font_color="#f1f5f9",
                           showlegend=False, margin=dict(t=40,b=10,l=10,r=10))
        fig2.update_traces(marker_line_width=0)
        st.plotly_chart(fig2, use_container_width=True)

with col_c:
    if total > 0:
        cat_counts = df.groupby("Category").size().reset_index(name="count").sort_values("count", ascending=True)
        fig3 = px.bar(
            cat_counts, x="count", y="Category",
            title="Tasks by Category", orientation="h",
            color="count",
            color_continuous_scale=["#3b0764","#7c3aed","#06b6d4"]
        )
        fig3.update_layout(**chart_theme, title_font_color="#f1f5f9",
                           coloraxis_showscale=False, margin=dict(t=40,b=10,l=10,r=10))
        st.plotly_chart(fig3, use_container_width=True)


# ─────────────────────────────────────────────
# Task List
# ─────────────────────────────────────────────
st.markdown(f"### 📝 Tasks &nbsp;<span style='font-size:0.85rem;color:#94a3b8;font-weight:400'>({len(filtered)} shown)</span>", unsafe_allow_html=True)

if filtered.empty:
    st.info("No tasks match the current filters.")
elif st.session_state.view_mode == "Table":
    display_df = filtered[["Title","Priority","Category","Due Date","Status"]].copy()
    display_df["Due Date"] = display_df["Due Date"].dt.strftime("%b %d, %Y")
    st.dataframe(display_df, use_container_width=True, hide_index=True)
else:
    # Card view
    for i, (idx, task) in enumerate(filtered.iterrows()):
        overdue_flag = is_overdue(task)
        card_class   = "completed" if task["Status"] == "Completed" else ("overdue" if overdue_flag else "")
        due_str      = pd.to_datetime(task["Due Date"]).strftime("%b %d, %Y")
        badge_html   = get_priority_badge(task["Priority"])
        status_badge = '<span class="badge badge-done">✓ Done</span>' if task["Status"] == "Completed" else \
                       ('<span class="badge badge-high">⚠ Overdue</span>' if overdue_flag else
                        '<span class="badge badge-low">● Pending</span>')

        st.markdown(
            f'<div class="task-card {card_class}">'
            f'<div style="display:flex;justify-content:space-between;align-items:flex-start;gap:1rem">'
            f'  <div>'
            f'    <div style="font-weight:600;font-size:1rem;color:#f1f5f9;margin-bottom:4px">{task["Title"]}</div>'
            f'    <div style="font-size:0.82rem;color:#94a3b8;margin-bottom:8px">{task["Description"] or "—"}</div>'
            f'    <div style="display:flex;gap:8px;flex-wrap:wrap;align-items:center">'
            f'      {badge_html}{status_badge}'
            f'      <span style="font-size:0.75rem;color:#64748b;font-family:JetBrains Mono,monospace">📅 {due_str}</span>'
            f'      <span style="font-size:0.75rem;color:#64748b">🏷 {task["Category"]}</span>'
            f'    </div>'
            f'  </div>'
            f'</div></div>',
            unsafe_allow_html=True
        )

        if task["Status"] == "Pending":
            btn_col, _ = st.columns([1, 4])
            with btn_col:
                if st.button("✓ Complete", key=f"done_{idx}_{i}"):
                    st.session_state.tasks.at[idx, "Status"] = "Completed"
                    st.rerun()


# ─────────────────────────────────────────────
# Footer
# ─────────────────────────────────────────────
st.markdown("---")
st.markdown(
    '<p style="text-align:center;color:#3f3f5a;font-size:0.75rem;">'
    'ProductivityOS · Built with Streamlit · by <strong style="color:#7c3aed">gideon-it-ug</strong>'
    '</p>',
    unsafe_allow_html=True
)

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date

# -----------------------------
# Initialize session state for tasks
# -----------------------------
if "tasks" not in st.session_state or not isinstance(st.session_state.tasks, pd.DataFrame):
    st.session_state.tasks = pd.DataFrame(columns=["Title", "Description", "Due Date", "Status"])

# -----------------------------
# Sidebar - Add new task
# -----------------------------
st.sidebar.header("➕ Add a New Task")
task_title = st.sidebar.text_input("Task Title")
task_desc = st.sidebar.text_area("Task Description")
task_due = st.sidebar.date_input("Due Date", min_value=date.today())
task_priority = st.sidebar.selectbox("Priority", ["Low", "Medium", "High"])

if st.sidebar.button("Add Task"):
    new_task = {
        "Title": task_title,
        "Description": task_desc + f" (Priority: {task_priority})",
        "Due Date": task_due,
        "Status": "Pending"
    }
    st.session_state.tasks = pd.concat([st.session_state.tasks, pd.DataFrame([new_task])], ignore_index=True)
    st.sidebar.success(f"Task '{task_title}' added!")

# -----------------------------
# Main Page - Dashboard
# -----------------------------
st.title("📊 Smart Employee Productivity Dashboard")
st.markdown("Track tasks, progress, and team productivity.")

# Metrics
total_tasks = len(st.session_state.tasks)
completed_tasks = len(st.session_state.tasks[st.session_state.tasks.Status == "Completed"])
overdue_tasks = len(st.session_state.tasks[(st.session_state.tasks.Status == "Pending") & 
                                          (st.session_state.tasks["Due Date"] < pd.to_datetime(date.today()))])

col1, col2, col3 = st.columns(3)
col1.metric("Total Tasks", total_tasks)
col2.metric("Completed Tasks", completed_tasks)
col3.metric("Overdue Tasks", overdue_tasks)

# -----------------------------
# Task Table with status update
# -----------------------------
st.subheader("📝 Current Tasks")
if not st.session_state.tasks.empty:
    for i in range(len(st.session_state.tasks)):
        task = st.session_state.tasks.iloc[i]
        st.write(f"**{task['Title']}** - {task['Description']}")
        st.write(f"Deadline: {task['Due Date'].date()} | Status: {task['Status']}")
        if task['Status'] == "Pending":
            if st.button(f"Mark '{task['Title']}' as Completed", key=i):
                st.session_state.tasks.at[i, "Status"] = "Completed"
                st.experimental_rerun()
        st.markdown("---")
else:
    st.info("No tasks added yet!")

# -----------------------------
# Filters
# -----------------------------
st.subheader("🔍 Filter Tasks")
status_filter = st.selectbox("Filter by Status", ["All", "Pending", "Completed"])
if status_filter != "All":
    filtered_tasks = st.session_state.tasks[st.session_state.tasks.Status == status_filter]
else:
    filtered_tasks = st.session_state.tasks
st.dataframe(filtered_tasks)

# -----------------------------
# Visual Analytics
# -----------------------------
st.subheader("📈 Task Analytics")
if total_tasks > 0:
    fig = px.pie(st.session_state.tasks, names='Status', title="Task Status Distribution")
    st.plotly_chart(fig)

    fig2 = px.bar(st.session_state.tasks, x='Due Date', color='Status', title="Tasks by Due Date")
    st.plotly_chart(fig2)

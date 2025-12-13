import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Initialize session state for tasks
if "tasks" not in st.session_state:
    st.session_state.tasks = []

# Title
st.title("Smart Employee Productivity Dashboard")
st.write("Track tasks, progress, and team productivity.")

# Task input form
st.subheader("Add a New Task")
with st.form(key="task_form"):
    employee = st.text_input("Employee Name")
    task = st.text_input("Task Description")
    deadline = st.date_input("Deadline")
    priority = st.selectbox("Priority", ["High", "Medium", "Low"])
    submitted = st.form_submit_button("Add Task")
    if submitted:
        new_task = {
            "Employee": employee,
            "Task": task,
            "Deadline": deadline,
            "Priority": priority,
            "Completed": False,
            "Date Added": datetime.today().date()
        }
        st.session_state.tasks.append(new_task)
        st.success("Task added successfully!")

# Display current tasks with editable completion status
st.subheader("Current Tasks")

if st.session_state.tasks:
    # Show tasks with checkboxes for completion
    for i, task in enumerate(st.session_state.tasks):
        cols = st.columns([3, 5, 2, 2, 2, 1])
        cols[0].write(task["Employee"])
        cols[1].write(task["Task"])
        cols[2].write(str(task["Deadline"]))
        cols[3].write(task["Priority"])
        # Checkbox to mark completed, updating session state
        completed = cols[4].checkbox("Completed", value=task["Completed"], key=f"completed_{i}")
        st.session_state.tasks[i]["Completed"] = completed

else:
    st.write("No tasks added yet.")

# Analytics
if st.session_state.tasks:
    df = pd.DataFrame(st.session_state.tasks)

    # Tasks per employee
    tasks_per_employee = df.groupby("Employee").size().reset_index(name="Number of Tasks")
    st.subheader("Tasks per Employee")
    st.dataframe(tasks_per_employee)

    # Task completion status
    completion_counts = df["Completed"].value_counts().reset_index()
    completion_counts.columns = ["Completed", "Count"]
    st.subheader("Task Completion Status")
    fig = px.pie(completion_counts, names="Completed", values="Count", title="Task Completion")
    st.plotly_chart(fig)

    # Overdue tasks
    today = datetime.today().date()
    overdue_tasks = df[(df["Deadline"] < today) & (df["Completed"] == False)]
    if not overdue_tasks.empty:
        st.subheader("⚠️ Overdue Tasks")
        st.dataframe(overdue_tasks)

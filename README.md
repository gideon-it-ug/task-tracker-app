# ⚡ ProductivityOS — Smart Task Dashboard

> A sleek, dark-themed productivity dashboard built with Streamlit, Pandas, and Plotly.

![Python](https://img.shields.io/badge/Python-3.10+-7c3aed?style=flat-square&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-06b6d4?style=flat-square&logo=streamlit&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-10b981?style=flat-square)

---

## ✨ Features

- **Task Management** — Add, filter, and complete tasks with priority levels, categories, and due dates
- **Live KPI Metrics** — Instant visibility into total, completed, pending, and overdue tasks
- **Visual Analytics** — Interactive Plotly charts: status breakdown, priority distribution, category analysis
- **Card + Table Views** — Switch between a rich card layout and a clean data table
- **Overdue Detection** — Tasks past their due date are automatically flagged
- **Progress Bar** — At-a-glance completion rate
- **Dark UI** — Custom CSS with Space Grotesk typography and a professional color palette

---

## 🚀 Quick Start

```bash
# Clone the repo
git clone https://github.com/gideon-it-ug/task-tracker-app.git
cd task-tracker-app

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run dashboard.py
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 📸 Dashboard Preview

| Section | Description |
|---|---|
| 🔢 KPI Row | Total, Completed, Pending, Overdue, and Completion % |
| 📊 Charts | Pie (status), Bar (priority), Horizontal bar (category) |
| 📝 Task Cards | Color-coded cards with priority badges and one-click completion |
| 🔍 Filters | Filter by Status, Priority, and Category from the sidebar |

---

## 🗂️ Project Structure

```
task-tracker-app/
├── dashboard.py        # Main Streamlit application
├── requirements.txt    # Python dependencies
└── README.md
```

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| [Streamlit](https://streamlit.io) | Web UI framework |
| [Pandas](https://pandas.pydata.org) | Data manipulation |
| [Plotly Express](https://plotly.com/python/plotly-express/) | Interactive charts |

---

## 👤 Author

**Mugabe Gideon** — [@gideon-it-ug](https://github.com/gideon-it-ug)

---

## 📄 License

MIT — free to use and modify.

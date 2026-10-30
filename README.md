# 🖥️ Logs MCP: Expense Tracker and System Health MCP Servers

Two small [Model Context Protocol](https://modelcontextprotocol.io/) servers built with [FastMCP](https://github.com/jlowin/fastmcp). Connect them to an MCP client such as Claude Desktop, and an AI assistant can log your expenses or produce a system health report for you.

![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)
![FastMCP](https://img.shields.io/badge/FastMCP-MCP_Server-6B4FBB)
![SQLite](https://img.shields.io/badge/SQLite-003B57?logo=sqlite&logoColor=white)

## 🧰 Servers

### `main.py`: Expense Tracker

Stores expenses in a local SQLite database (`expenses.db`).

| Tool | What it does |
|---|---|
| `add_expense(amount, category, notes)` | Records an expense with today's date |
| `list_expenses(start_date, end_date)` | Lists expenses in a date range (defaults to the last 7 days) |
| `summarize_expenses(category)` | Shows the total for one category, or a breakdown of all categories |

### `system_tools.py`: System Health

Uses `psutil` to read CPU, RAM, disk and uptime.

| Tool / Prompt | What it does |
|---|---|
| `open_dashboard_workflow(recipient)` | Builds a dark-themed HTML health dashboard, saves it to `~/Documents`, and opens it in the browser along with a pre-filled Gmail draft and a Google Calendar maintenance event |
| `technician_report` (prompt) | A ready-made prompt that runs the dashboard workflow |

## 🚀 Getting Started

This project uses [uv](https://docs.astral.sh/uv/).

```bash
uv sync
uv run system_tools.py     # serves over HTTP on port 8000
```

Or add a server to your MCP client's config, for example:

```json
{
  "mcpServers": {
    "expense-tracker": {
      "command": "uv",
      "args": ["run", "fastmcp", "run", "main.py"]
    }
  }
}
```

> **Note:** the disk check in `system_tools.py` reads the `C:\` drive, so it is written for Windows. On other systems the disk metric shows as N/A.

## 📦 Requirements

- Python 3.13+
- `fastmcp`, `psutil` (see `pyproject.toml`)

from fastmcp import FastMCP
import sqlite3
from datetime import datetime, timedelta

# Initialize
mcp = FastMCP("expense-tracker")
DB_FILE = "expenses.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL,
            category TEXT,
            notes TEXT,
            date TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# --- TOOL 1: ADD EXPENSE ---
@mcp.tool()
def add_expense(amount: float, category: str, notes: str) -> str:
    """
    Add a new expense.
    Args:
        amount: Cost of the item.
        category: Category (e.g., Food, Transport, Shopping).
        notes: Description of the purchase.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    date_str = datetime.now().strftime("%Y-%m-%d")
    cursor.execute(
        "INSERT INTO expenses (amount, category, notes, date) VALUES (?, ?, ?, ?)",
        (amount, category, notes, date_str)
    )
    conn.commit()
    conn.close()
    return f"Added: ${amount} for {category} ({notes})"

# --- TOOL 2: LIST EXPENSES (With Date Filter) ---
@mcp.tool()
def list_expenses(start_date: str = None, end_date: str = None) -> str:
    """
    List expenses, optionally filtered by date range.
    Args:
        start_date: YYYY-MM-DD (Defaults to 7 days ago if not provided)
        end_date: YYYY-MM-DD (Defaults to today)
    """
    # Default to last 7 days if no date provided
    if not start_date:
        start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    if not end_date:
        end_date = datetime.now().strftime("%Y-%m-%d")

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM expenses WHERE date BETWEEN ? AND ?", 
        (start_date, end_date)
    )
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        return f"No expenses found between {start_date} and {end_date}."

    report = f"Expenses from {start_date} to {end_date}:\n"
    for row in rows:
        report += f"- {row[4]}: ${row[1]} ({row[2]}) | {row[3]}\n"
    return report

# --- TOOL 3: SUMMARIZE (The "Useful" Feature) ---
@mcp.tool()
def summarize_expenses(category: str = None) -> str:
    """
    Calculate total spending.
    Args:
        category: (Optional) Filter by a specific category like 'Food'.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    if category:
        cursor.execute("SELECT SUM(amount) FROM expenses WHERE category = ?", (category,))
        result = cursor.fetchone()[0]
        msg = f"Total spent on {category}: ${result or 0}"
    else:
        cursor.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
        rows = cursor.fetchall()
        msg = "Spending Breakdown:\n"
        total = 0
        for cat, amount in rows:
            msg += f"- {cat}: ${amount}\n"
            total += amount
        msg += f"\nTOTAL SPENT: ${total}"

    conn.close()
    return msg
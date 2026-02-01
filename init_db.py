import sqlite3

conn = sqlite3.connect("budget.db")
conn.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item TEXT,
    amount REAL,
    date TEXT
)
""")
conn.close()

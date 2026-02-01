from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)
DB_FILE = "budget.db"


def get_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/", methods=["GET", "POST"])
def index():
    conn = get_db()
    cur = conn.cursor()

    if request.method == "POST":
        item = request.form["item"]
        amount = float(request.form["amount"])
        date = datetime.now().strftime("%Y-%m-%d")

        cur.execute(
            "INSERT INTO expenses (item, amount, date) VALUES (?, ?, ?)",
            (item, amount, date),
        )
        conn.commit()
        return redirect("/")

    cur.execute("""
        SELECT item, amount, date
        FROM expenses
        WHERE strftime('%Y-%m', date) = strftime('%Y-%m', 'now')
        ORDER BY date DESC
    """)
    expenses = cur.fetchall()

    cur.execute("""
        SELECT SUM(amount) as total
        FROM expenses
        WHERE strftime('%Y-%m', date) = strftime('%Y-%m', 'now')
    """)
    total = cur.fetchone()["total"] or 0

    conn.close()
    return render_template("index.html", expenses=expenses, total=total)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

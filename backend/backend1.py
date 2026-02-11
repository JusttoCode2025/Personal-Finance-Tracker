from flask import Flask, request, jsonify, render_template
import sqlite3
from datetime import datetime

app = Flask(__name__)
DB_NAME = "finance_tracker.db"

# --------------------
# Database setup
# --------------------
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS spending_limits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT NOT NULL UNIQUE,
        limit_amount REAL NOT NULL,
        remaining REAL NOT NULL
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS purchases (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT NOT NULL,
        amount REAL NOT NULL,
        date TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()

init_db()

# --------------------
# Helpers
# --------------------
def db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

# --------------------
# Routes
# --------------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/limit", methods=["POST"])
def set_limit():
    data = request.get_json()
    category = data.get("category").strip().lower()
    limit_amount = float(data.get("limit_amount"))

    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM spending_limits WHERE category=?", (category,))
    row = cursor.fetchone()
    if row:
        cursor.execute("UPDATE spending_limits SET limit_amount=?, remaining=? WHERE id=?", (limit_amount, limit_amount, row["id"]))
    else:
        cursor.execute("INSERT INTO spending_limits (category, limit_amount, remaining) VALUES (?, ?, ?)", (category, limit_amount, limit_amount))
    conn.commit()
    conn.close()
    return jsonify({"message": f"Limit set for {category}: ${limit_amount}"}), 200

@app.route("/purchase", methods=["POST"])
def add_purchase():  #user can put negative amount to gain money
    data = request.get_json()
    category = data.get("category").strip().lower()
    amount = float(data.get("amount"))

    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT remaining FROM spending_limits WHERE category=?", (category,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return jsonify({"error": f"No limit set for category '{category}'"}), 400

    remaining = row["remaining"]
    new_remaining = remaining - amount
    cursor.execute("UPDATE spending_limits SET remaining=? WHERE category=?", (new_remaining, category))
    cursor.execute("INSERT INTO purchases (category, amount, date) VALUES (?, ?, ?)",
                   (category, amount, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

    response = {"message": f"Purchase of ${amount} recorded in '{category}'", "remaining": new_remaining}
    if amount > remaining:
        response["warning"] = f"Purchase exceeds remaining limit (${remaining})!"
    return jsonify(response), 200

@app.route("/limits", methods=["GET"])
def view_limits():
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT category, limit_amount, remaining FROM spending_limits")
    rows = cursor.fetchall()
    conn.close()
    limits = [{"category": r["category"], "limit_amount": r["limit_amount"], "remaining": r["remaining"]} for r in rows]
    return jsonify(limits), 200

# --------------------
# Run app
# --------------------
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)



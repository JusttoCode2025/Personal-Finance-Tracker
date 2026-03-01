from flask import Flask, request, jsonify, render_template, redirect
import sqlite3
from datetime import datetime

app = Flask(
    __name__,
    template_folder="../frontend/templates",
    static_folder="../frontend/static"
)
DB_NAME = "finance_tracker1.db"


#DATABASE SETUP

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


def db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


# PAGE ROUTE

@app.route("/")
@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/budget")
def budget():
    return render_template("budget.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")


#  API

@app.route("/limit", methods=["POST"])
def set_limit():
    """
    Set or update a spending limit for a category
    """
    data = request.get_json()
    category = data.get("category", "").strip().lower()
    limit_amount = float(data.get("limit_amount", 0))

    if limit_amount <= 0:
        return jsonify({"error": "Limit amount must be positive"}), 400

    conn = db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM spending_limits WHERE category=?",
        (category,)
    )
    row = cursor.fetchone()

    if row:
        cursor.execute(
            "UPDATE spending_limits SET limit_amount=?, remaining=? WHERE id=?",
            (limit_amount, limit_amount, row["id"])
        )
    else:
        cursor.execute(
            "INSERT INTO spending_limits (category, limit_amount, remaining) VALUES (?, ?, ?)",
            (category, limit_amount, limit_amount)
        )

    conn.commit()
    conn.close()

    return jsonify({
        "message": f"Limit set for '{category}'",
        "limit_amount": limit_amount
    }), 200

@app.route("/recent_purchases", methods=["GET"])
def recent_purchases():
    conn = db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT category, amount, date
        FROM purchases
        ORDER BY date DESC
        LIMIT 5
    """)

    rows = cursor.fetchall()
    conn.close()

    purchases = [
        {
            "category": r["category"],
            "amount": r["amount"],
            "date": r["date"]
        }
        for r in rows
    ]

    return jsonify(purchases), 200

@app.route("/purchase", methods=["POST"])
def add_purchase():
    """
    Add a purchase and deduct from category limit
    """
    data = request.get_json()
    category = data.get("category", "").strip().lower()
    amount = float(data.get("amount", 0))

    if amount <= 0:
        return jsonify({"error": "Purchase amount must be positive"}), 400

    conn = db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT remaining FROM spending_limits WHERE category=?",
        (category,)
    )
    row = cursor.fetchone()

    if not row:
        conn.close()
        return jsonify({
            "error": f"No limit set for category '{category}'"
        }), 400

    remaining = row["remaining"]
    new_remaining = remaining - amount

    cursor.execute(
        "UPDATE spending_limits SET remaining=? WHERE category=?",
        (new_remaining, category)
    )

    cursor.execute(
        "INSERT INTO purchases (category, amount, date) VALUES (?, ?, ?)",
        (category, amount, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )

    conn.commit()
    conn.close()

    response = {
        "message": f"Purchase of ${amount} recorded",
        "category": category,
        "remaining": new_remaining
    }

    if new_remaining < 0:
        response["warning"] = "You have exceeded the category limit!"

    return jsonify(response), 200


@app.route("/limits", methods=["GET"])
def view_limits():
    """
    View all category limits and remaining balances
    """
    conn = db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT category, limit_amount, remaining FROM spending_limits"
    )
    rows = cursor.fetchall()
    conn.close()

    limits = [{
        "category": r["category"],
        "limit_amount": r["limit_amount"],
        "remaining": r["remaining"],
        "spent": r["limit_amount"] - r["remaining"]
    } for r in rows]

    return jsonify(limits), 200


if __name__ == "__main__":
    app.run(debug=True)








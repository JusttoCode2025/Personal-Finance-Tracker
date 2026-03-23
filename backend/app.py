from flask import Flask, request, jsonify, render_template
import psycopg2
import os
from datetime import datetime

app = Flask(
    __name__,
    template_folder="../frontend/templates",
    static_folder="../frontend/static"
)

DATABASE_URL = os.environ.get("DATABASE_URL")

if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

def db_connection():
    return psycopg2.connect(DATABASE_URL)

# ======================
# INIT DATABASE
# ======================
def init_db():
    conn = db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS spending_limits (
        id SERIAL PRIMARY KEY,
        category TEXT UNIQUE NOT NULL,
        limit_amount REAL NOT NULL,
        remaining REAL NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS purchases (
        id SERIAL PRIMARY KEY,
        category TEXT NOT NULL,
        amount REAL NOT NULL,
        date TIMESTAMP NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS travel_goal (
        id SERIAL PRIMARY KEY,
        goal_amount REAL NOT NULL,
        saved_amount REAL DEFAULT 0
    )
    """)

    conn.commit()
    cursor.close()
    conn.close()

init_db()

# ======================
# ROUTES
# ======================
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

@app.route("/travel-goal")
def travel_goal():
    return render_template("travel_goal.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

# ======================
# API
# ======================
@app.route("/recent_purchases")
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
    cursor.close()
    conn.close()

    return jsonify([
        {"category": r[0], "amount": float(r[1]), "date": str(r[2])}
        for r in rows
    ])

@app.route("/limit", methods=["POST"])
def set_limit():
    data = request.get_json()
    category = data.get("category").lower()
    limit = float(data.get("limit_amount"))

    conn = db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM spending_limits WHERE category=%s", (category,))
    row = cursor.fetchone()

    if row:
        cursor.execute(
            "UPDATE spending_limits SET limit_amount=%s, remaining=%s WHERE id=%s",
            (limit, limit, row[0])
        )
    else:
        cursor.execute(
            "INSERT INTO spending_limits VALUES (DEFAULT, %s, %s, %s)",
            (category, limit, limit)
        )

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Limit set"})

@app.route("/purchase", methods=["POST"])
def purchase():
    data = request.get_json()
    category = data["category"]
    amount = float(data["amount"])
    confirm = data.get("confirm", False)

    conn = db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT remaining FROM spending_limits WHERE category=%s", (category,))
    row = cursor.fetchone()

    if not row:
        return jsonify({"error": "No limit set"})

    remaining = float(row[0])
    new_remaining = remaining - amount

    if new_remaining < 0 and not confirm:
        return jsonify({"warning": "Exceeds limit"})

    cursor.execute("UPDATE spending_limits SET remaining=%s WHERE category=%s", (new_remaining, category))
    cursor.execute("INSERT INTO purchases VALUES (DEFAULT, %s, %s, %s)", (category, amount, datetime.now()))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Purchase added"})

@app.route("/limits")
def limits():
    conn = db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT category, limit_amount, remaining FROM spending_limits")
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify([
        {
            "category": r[0],
            "limit_amount": float(r[1]),
            "remaining": float(r[2]),
            "spent": float(r[1]) - float(r[2])
        }
        for r in rows
    ])

@app.route("/dashboard_data")
def dashboard_data():
    conn = db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COALESCE(SUM(amount),0) FROM purchases")
    total = float(cursor.fetchone()[0])

    cursor.execute("SELECT category, SUM(amount) FROM purchases GROUP BY category")
    categories = [{"category": r[0], "total": float(r[1])} for r in cursor.fetchall()]

    cursor.execute("""
        SELECT TO_CHAR(date,'YYYY-MM'), SUM(amount)
        FROM purchases GROUP BY 1 ORDER BY 1 DESC LIMIT 12
    """)
    monthly = [{"month": r[0], "total": float(r[1])} for r in cursor.fetchall()]

    cursor.close()
    conn.close()

    return jsonify({"total_spent": total, "categories": categories, "monthly": monthly})

# ======================
# TRAVEL GOAL
# ======================
@app.route("/travel_goal/set", methods=["POST"])
def set_goal():
    data = request.get_json()
    goal = float(data["goal_amount"])

    conn = db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM travel_goal")
    cursor.execute("INSERT INTO travel_goal VALUES (DEFAULT, %s, 0)", (goal,))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Goal set"})

@app.route("/travel_goal/add", methods=["POST"])
def add_goal():
    data = request.get_json()
    amount = float(data["amount"])

    conn = db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE travel_goal
        SET saved_amount = saved_amount + %s
        RETURNING goal_amount, saved_amount
    """, (amount,))

    row = cursor.fetchone()

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({
        "goal_amount": float(row[0]),
        "saved_amount": float(row[1]),
        "remaining": float(row[0]) - float(row[1])
    })

@app.route("/travel_goal")
def get_goal():
    conn = db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT goal_amount, saved_amount FROM travel_goal LIMIT 1")
    row = cursor.fetchone()

    cursor.close()
    conn.close()

    if not row:
        return jsonify({"message": "No goal set"})

    return jsonify({
        "goal_amount": float(row[0]),
        "saved_amount": float(row[1]),
        "remaining": float(row[0]) - float(row[1])
    })

@app.route("/travel_goal/reset", methods=["POST"])
def reset_goal():
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM travel_goal")
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "reset"})


if __name__ == "__main__":
    app.run(debug=True)

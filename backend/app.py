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
    CREATE TABLE IF NOT EXISTS travel_goals (
        id SERIAL PRIMARY KEY,
        destination TEXT NOT NULL,
        target_amount REAL NOT NULL,
        saved_amount REAL DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        note TEXT DEFAULT '',
        target_date DATE DEFAULT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS settings (
        id SERIAL PRIMARY KEY,
        budget_reset_at TIMESTAMP DEFAULT NULL
    )
    """)

    cursor.execute("SELECT COUNT(*) FROM settings")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO settings (budget_reset_at) VALUES (NULL)")

    cursor.execute("ALTER TABLE travel_goals ADD COLUMN IF NOT EXISTS note TEXT DEFAULT ''")
    cursor.execute("ALTER TABLE travel_goals ADD COLUMN IF NOT EXISTS target_date DATE DEFAULT NULL")

    conn.commit()
    cursor.close()
    conn.close()


init_db()


def get_budget_reset_at(cursor):
    cursor.execute("SELECT budget_reset_at FROM settings LIMIT 1")
    row = cursor.fetchone()
    return row[0] if row and row[0] else None


# HTML routes
@app.route("/")
@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/budget")
def budget():
    return render_template("budget.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/travel-goal")
def travel_goal():
    return render_template("travel_goal.html")


# New month — updates reset timestamp and resets remaining to full limits
@app.route("/new_month", methods=["POST"])
def new_month():
    conn = db_connection()
    cursor = conn.cursor()

    now = datetime.now()
    cursor.execute("UPDATE settings SET budget_reset_at = %s", (now,))
    cursor.execute("UPDATE spending_limits SET remaining = limit_amount")

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "New month started", "reset_at": str(now)}), 200


@app.route("/settings")
def get_settings():
    conn = db_connection()
    cursor = conn.cursor()
    reset_at = get_budget_reset_at(cursor)
    cursor.close()
    conn.close()
    return jsonify({"budget_reset_at": str(reset_at) if reset_at else None})


@app.route("/recent_purchases")
def recent_purchases():
    conn = db_connection()
    cursor = conn.cursor()

    reset_at = get_budget_reset_at(cursor)

    if reset_at:
        cursor.execute("""
            SELECT category, amount, date
            FROM purchases
            WHERE date >= %s
            ORDER BY date DESC
            LIMIT 5
        """, (reset_at,))
    else:
        cursor.execute("""
            SELECT category, amount, date
            FROM purchases
            WHERE DATE_TRUNC('month', date) = DATE_TRUNC('month', CURRENT_DATE)
            ORDER BY date DESC
            LIMIT 5
        """)

    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    purchases = [
        {"category": r[0], "amount": float(r[1]), "date": str(r[2])}
        for r in rows
    ]

    return jsonify(purchases)


# Set or update category limit
@app.route("/limit", methods=["POST"])
def set_limit():
    data = request.get_json()
    category = data.get("category", "").strip().lower()
    limit_amount = float(data.get("limit_amount", 0))

    if limit_amount <= 0:
        return jsonify({"error": "Limit amount must be positive"}), 400

    conn = db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, remaining, limit_amount FROM spending_limits WHERE category=%s", (category,))
    row = cursor.fetchone()

    if row:
        old_limit = float(row[2])
        old_remaining = float(row[1])
        spent = old_limit - old_remaining

        if limit_amount < spent:
            cursor.close()
            conn.close()
            return jsonify({"error": f"Cannot set limit below amount already spent (${spent:.2f})"}), 400

        cursor.execute(
            "UPDATE spending_limits SET limit_amount=%s, remaining=%s WHERE id=%s",
            (limit_amount, limit_amount - spent, row[0])
        )
    else:
        cursor.execute(
            "INSERT INTO spending_limits (category, limit_amount, remaining) VALUES (%s, %s, %s)",
            (category, limit_amount, limit_amount)
        )

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": f"Limit set for '{category}'", "limit_amount": limit_amount}), 200


@app.route("/purchase", methods=["POST"])
def add_purchase():
    data = request.get_json()
    category = data.get("category", "").strip().lower()
    amount = float(data.get("amount", 0))
    confirm = data.get("confirm", False)

    if amount <= 0:
        return jsonify({"error": "Purchase amount must be positive"}), 400

    conn = db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT remaining FROM spending_limits WHERE category=%s", (category,))
    row = cursor.fetchone()

    if not row:
        cursor.close()
        conn.close()
        return jsonify({"error": f"No limit set for category '{category}'"}), 400

    remaining = float(row[0])
    new_remaining = remaining - amount

    if new_remaining < 0 and not confirm:
        cursor.close()
        conn.close()
        return jsonify({"warning": "This purchase exceeds the category limit. Continue anyway?"}), 200

    cursor.execute("UPDATE spending_limits SET remaining=%s WHERE category=%s", (new_remaining, category))
    cursor.execute("INSERT INTO purchases (category, amount, date) VALUES (%s, %s, %s)", (category, amount, datetime.now()))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": f"Purchase of ${amount} recorded", "category": category, "remaining": new_remaining}), 200


@app.route("/limits", methods=["GET"])
def view_limits():
    conn = db_connection()
    cursor = conn.cursor()

    reset_at = get_budget_reset_at(cursor)

    if reset_at:
        # Filter purchases since the last New Month reset
        cursor.execute("""
            SELECT s.category, s.limit_amount,
                   COALESCE(SUM(p.amount), 0) as spent_since_reset
            FROM spending_limits s
            LEFT JOIN purchases p
                ON p.category = s.category AND p.date >= %s
            GROUP BY s.category, s.limit_amount
        """, (reset_at,))
    else:
        # No reset yet — default to current month only
        cursor.execute("""
            SELECT s.category, s.limit_amount,
                   COALESCE(SUM(p.amount), 0) as spent_since_reset
            FROM spending_limits s
            LEFT JOIN purchases p
                ON p.category = s.category
                AND DATE_TRUNC('month', p.date) = DATE_TRUNC('month', CURRENT_DATE)
            GROUP BY s.category, s.limit_amount
        """)

    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    limits = [{
        "category": r[0],
        "limit_amount": float(r[1]),
        "remaining": float(r[1]) - float(r[2]),
        "spent": float(r[2])
    } for r in rows]

    return jsonify(limits), 200


@app.route("/dashboard_data")
def dashboard_data():
    conn = db_connection()
    cursor = conn.cursor()

    month_param = request.args.get("month")

    if month_param:
        try:
            selected = datetime.strptime(month_param, "%Y-%m")
            month_filter = f"DATE_TRUNC('month', date) = '{selected.strftime('%Y-%m-01')}'"
        except ValueError:
            month_filter = "DATE_TRUNC('month', date) = DATE_TRUNC('month', CURRENT_DATE)"
    else:
        month_filter = "DATE_TRUNC('month', date) = DATE_TRUNC('month', CURRENT_DATE)"

    cursor.execute(f"SELECT COALESCE(SUM(amount), 0) FROM purchases WHERE {month_filter}")
    total_spent = float(cursor.fetchone()[0])

    cursor.execute(f"""
        SELECT category, amount, date FROM purchases
        WHERE {month_filter}
        ORDER BY amount DESC LIMIT 1
    """)
    biggest_row = cursor.fetchone()
    biggest_expense = {
        "category": biggest_row[0],
        "amount": float(biggest_row[1]),
        "date": str(biggest_row[2])
    } if biggest_row else None

    cursor.execute(f"""
        SELECT category, SUM(amount)
        FROM purchases
        WHERE {month_filter}
        GROUP BY category
    """)
    category_rows = cursor.fetchall()
    categories = [{"category": r[0], "total": float(r[1])} for r in category_rows]

    cursor.execute("""
        SELECT TO_CHAR(date, 'YYYY-MM-DD') as day, SUM(amount)
        FROM purchases
        WHERE date >= CURRENT_DATE - INTERVAL '30 days'
        GROUP BY day
        ORDER BY day ASC
    """)
    monthly_rows = cursor.fetchall()
    monthly = [{"month": r[0], "total": float(r[1])} for r in monthly_rows]

    cursor.execute("""
        SELECT DISTINCT TO_CHAR(date, 'YYYY-MM') as month
        FROM purchases
        ORDER BY month DESC
    """)
    available_months = [r[0] for r in cursor.fetchall()]

    cursor.execute("""
        SELECT s.category, s.limit_amount, s.remaining
        FROM spending_limits s
        WHERE s.remaining >= 0
        ORDER BY (s.limit_amount - s.remaining) / NULLIF(s.limit_amount, 0) DESC
        LIMIT 1
    """)
    warn_row = cursor.fetchone()
    closest_to_limit = {
        "category": warn_row[0],
        "limit_amount": float(warn_row[1]),
        "remaining": float(warn_row[2]),
        "pct_used": round(((float(warn_row[1]) - float(warn_row[2])) / float(warn_row[1])) * 100, 1)
    } if warn_row else None

    cursor.close()
    conn.close()

    return jsonify({
        "total_spent": total_spent,
        "categories": categories,
        "monthly": monthly,
        "biggest_expense": biggest_expense,
        "closest_to_limit": closest_to_limit,
        "available_months": available_months
    })


# Travel goal routes

@app.route("/travel_goal", methods=["POST"])
def add_travel_goal():
    data = request.get_json()
    destination = data.get("destination", "My Trip")
    target_amount = float(data.get("target_amount", 0))
    target_date = data.get("target_date", None)

    conn = db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM travel_goals")
    cursor.execute(
        "INSERT INTO travel_goals (destination, target_amount, saved_amount, note, target_date) VALUES (%s, %s, 0, '', %s)",
        (destination, target_amount, target_date)
    )

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Goal created"}), 200


@app.route("/travel_goals", methods=["GET"])
def get_travel_goals():
    conn = db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, destination, target_amount, saved_amount, created_at, note, target_date
        FROM travel_goals
        ORDER BY created_at DESC
    """)

    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify([
        {
            "id": r[0],
            "destination": r[1],
            "target_amount": float(r[2]),
            "saved_amount": float(r[3]),
            "created_at": str(r[4]),
            "note": r[5] or "",
            "target_date": str(r[6]) if r[6] else None
        }
        for r in rows
    ])


@app.route("/travel_goal/note", methods=["POST"])
def save_note():
    data = request.get_json()
    goal_id = data.get("id")
    note = data.get("note", "")

    if not goal_id:
        return jsonify({"error": "Invalid goal ID"}), 400

    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE travel_goals SET note=%s WHERE id=%s", (note, goal_id))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Note saved"}), 200


@app.route("/travel_goal/date", methods=["POST"])
def save_target_date():
    data = request.get_json()
    goal_id = data.get("id")
    target_date = data.get("target_date", None)

    if not goal_id:
        return jsonify({"error": "Invalid goal ID"}), 400

    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE travel_goals SET target_date=%s WHERE id=%s", (target_date, goal_id))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Target date saved"}), 200


@app.route("/travel_goal/save", methods=["POST"])
def update_savings():
    data = request.get_json()
    goal_id = data.get("id")
    amount = float(data.get("amount", 0))

    if not goal_id or amount <= 0:
        return jsonify({"error": "Invalid input"}), 400

    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE travel_goals SET saved_amount = saved_amount + %s WHERE id = %s", (amount, goal_id))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Savings updated"}), 200


@app.route("/travel_goal/reset", methods=["POST"])
def reset_travel_goal():
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM travel_goals")
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Reset successful"}), 200


@app.route("/transfer_to_travel", methods=["POST"])
def transfer_to_travel():
    conn = db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COALESCE(SUM(remaining), 0) FROM spending_limits")
    total_remaining = float(cursor.fetchone()[0])

    if total_remaining <= 0:
        cursor.close()
        conn.close()
        return jsonify({"error": "No remaining budget to transfer"}), 400

    cursor.execute("SELECT id FROM travel_goals LIMIT 1")
    goal = cursor.fetchone()

    if not goal:
        cursor.close()
        conn.close()
        return jsonify({"error": "Please set a travel goal first"}), 400

    cursor.execute("UPDATE travel_goals SET saved_amount = saved_amount + %s WHERE id = %s", (total_remaining, goal[0]))
    cursor.execute("UPDATE spending_limits SET remaining = 0")

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": f"${total_remaining:.2f} transferred to travel goal"}), 200


# Seed realistic test data — REMOVE AFTER USE
@app.route("/seed_data")
def seed_data():
    conn = db_connection()
    cursor = conn.cursor()

    test_data = [
        # January 2026
        ("rent",           1500, "2026-01-01"),
        ("groceries",       120, "2026-01-04"),
        ("utilities",        85, "2026-01-06"),
        ("groceries",        95, "2026-01-11"),
        ("transportation",   45, "2026-01-13"),
        ("entertainment",    60, "2026-01-15"),
        ("groceries",       210, "2026-01-19"),
        ("transportation",   30, "2026-01-22"),
        ("entertainment",    35, "2026-01-25"),
        ("other",            50, "2026-01-28"),
        # February 2026
        ("rent",           1500, "2026-02-01"),
        ("utilities",        92, "2026-02-03"),
        ("groceries",       130, "2026-02-06"),
        ("entertainment",    456, "2026-02-08"),
        ("groceries",        100, "2026-02-12"),
        ("transportation",   55, "2026-02-14"),
        ("other",            700, "2026-02-17"),
        ("groceries",       150, "2026-02-20"),
        ("entertainment",    50, "2026-02-22"),
        ("transportation",   25, "2026-02-26"),
        # March 2026
        ("rent",           1500, "2026-03-01"),
        ("utilities",        78, "2026-03-03"),
        ("groceries",       145, "2026-03-05"),
        ("transportation",   60, "2026-03-08"),
        ("entertainment",    90, "2026-03-10"),
        ("groceries",       115, "2026-03-14"),
        ("other",            65, "2026-03-16"),
        ("groceries",        80, "2026-03-20"),
        ("transportation",   40, "2026-03-23"),
        ("entertainment",    55, "2026-03-27"),
        # April 2026
        ("rent",           1500, "2026-04-01"),
        ("utilities",        88, "2026-04-02"),
        ("groceries",       125, "2026-04-04"),
        ("transportation",   50, "2026-04-07"),
        ("groceries",        95, "2026-04-10"),
        ("entertainment",    70, "2026-04-12"),
        ("other",            30, "2026-04-15"),
        ("groceries",       105, "2026-04-18"),
        ("transportation",   35, "2026-04-20"),
        ("entertainment",    45, "2026-04-22"),
    ]

    for category, amount, date in test_data:
        cursor.execute(
            "INSERT INTO purchases (category, amount, date) VALUES (%s, %s, %s)",
            (category, amount, date)
        )

    # Seed spending limits
    limits = [
        ("rent",           1500),
        ("groceries",       500),
        ("utilities",       200),
        ("transportation",  150),
        ("entertainment",   200),
        ("other",           250),
    ]
    for category, limit in limits:
        cursor.execute(
            "INSERT INTO spending_limits (category, limit_amount, remaining) VALUES (%s, %s, %s) ON CONFLICT (category) DO NOTHING",
            (category, limit, limit)
        )

    conn.commit()
    cursor.close()
    conn.close()
    return "Test data added!"


@app.route("/clear_db")
def clear_db():
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM purchases")
    cursor.execute("DELETE FROM spending_limits")
    cursor.execute("DELETE FROM travel_goals")
    cursor.execute("UPDATE settings SET budget_reset_at = NULL")
    conn.commit()
    cursor.close()
    conn.close()
    return "Database cleared!"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

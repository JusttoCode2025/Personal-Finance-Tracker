
from flask import Flask, request, jsonify, render_template
import psycopg2
import os
from datetime import datetime

app = Flask(
    __name__,
    template_folder="../frontend/templates",
    static_folder="../frontend/static"
)

#  dbs connect to render 
DATABASE_URL = os.environ.get("DATABASE_URL")

if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

def db_connection():
    return psycopg2.connect(DATABASE_URL)

#creation of dbs
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
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    cursor.close()
    conn.close()


init_db()


#html routes
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

    purchases = [
        {
            "category": r[0],
            "amount": float(r[1]),
            "date": str(r[2])
        }
        for r in rows
    ]

    return jsonify(purchases)


@app.route("/limit", methods=["POST"])
def set_limit():
    data = request.get_json()
    category = data.get("category", "").strip().lower()
    limit_amount = float(data.get("limit_amount", 0))

    if limit_amount <= 0:
        return jsonify({"error": "Limit amount must be positive"}), 400

    conn = db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM spending_limits WHERE category=%s",
        (category,)
    )
    row = cursor.fetchone()

    if row:
        cursor.execute(
            "UPDATE spending_limits SET limit_amount=%s, remaining=%s WHERE id=%s",
            (limit_amount, limit_amount, row[0])
        )
    else:
        cursor.execute(
            "INSERT INTO spending_limits (category, limit_amount, remaining) VALUES (%s, %s, %s)",
            (category, limit_amount, limit_amount)
        )

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({
        "message": f"Limit set for '{category}'",
        "limit_amount": limit_amount
    }), 200


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

    cursor.execute(
        "SELECT remaining FROM spending_limits WHERE category=%s",
        (category,)
    )
    row = cursor.fetchone()

    if not row:
        cursor.close()
        conn.close()
        return jsonify({
            "error": f"No limit set for category '{category}'"
        }), 400

    remaining = float(row[0])
    new_remaining = remaining - amount

    if new_remaining < 0 and not confirm:
        cursor.close()
        conn.close()
        return jsonify({
            "warning": "This purchase exceeds the category limit. Continue anyway?"
        }), 200
        
    cursor.execute(
        "UPDATE spending_limits SET remaining=%s WHERE category=%s",
        (new_remaining, category)
    )

    cursor.execute(
        "INSERT INTO purchases (category, amount, date) VALUES (%s, %s, %s)",
        (category, amount, datetime.now())
    )

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({
        "message": f"Purchase of ${amount} recorded",
        "category": category,
        "remaining": new_remaining
    }), 200


@app.route("/limits", methods=["GET"])
def view_limits():
    conn = db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT category, limit_amount, remaining FROM spending_limits"
    )
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    limits = [{
        "category": r[0],
        "limit_amount": float(r[1]),
        "remaining": float(r[2]),
        "spent": float(r[1]) - float(r[2])
    } for r in rows]

    return jsonify(limits), 200


@app.route("/dashboard_data")
def dashboard_data():
    conn = db_connection()  
    cursor = conn.cursor()

    cursor.execute("SELECT COALESCE(SUM(amount), 0) FROM purchases")
    total_spent = float(cursor.fetchone()[0])

    cursor.execute("""
        SELECT category, SUM(amount)
        FROM purchases
        GROUP BY category
    """)
    category_rows = cursor.fetchall()

    categories = [
        {"category": r[0], "total": float(r[1])}
        for r in category_rows
    ]

    cursor.execute("""
        SELECT TO_CHAR(date, 'YYYY-MM') as month, SUM(amount)
        FROM purchases
        GROUP BY month
        ORDER BY month DESC
        LIMIT 12
    """)
    monthly_rows = cursor.fetchall()

    monthly = [
        {"month": r[0], "total": float(r[1])}
        for r in monthly_rows
    ]

    cursor.close()
    conn.close()

    return jsonify({
        "total_spent": total_spent,
        "categories": categories,
        "monthly": monthly
    })
# reset
@app.route('/reset_categories', methods=['POST'])
def reset_categories():
    db.session.query(Limit).delete()
    db.session.query(Purchase).delete()
    db.session.commit()
    return jsonify({'success': True})


#travel goal

@app.route("/travel_goal", methods=["POST"])
def add_travel_goal():
    data = request.get_json()

    destination = data.get("destination", "My Trip")
    target_amount = float(data.get("target_amount", 0))

    conn = db_connection()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM travel_goals")
    
    cursor.execute(
        "INSERT INTO travel_goals (destination, target_amount, saved_amount) VALUES (%s, %s, 0)",
        (destination, target_amount)
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
        SELECT id, destination, target_amount, saved_amount, created_at
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
            "created_at": str(r[4])
        }
        for r in rows
    ])


@app.route("/travel_goal/save", methods=["POST"])
def update_savings():
    data = request.get_json()

    goal_id = data.get("id")
    amount = float(data.get("amount", 0))

    if not goal_id or amount <= 0:
        return jsonify({"error": "Invalid input"}), 400

    conn = db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE travel_goals
        SET saved_amount = saved_amount + %s
        WHERE id = %s
    """, (amount, goal_id))

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

#transfer to travel route 
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

    
    cursor.execute("""
        UPDATE travel_goals
        SET saved_amount = saved_amount + %s
        WHERE id = %s
    """, (total_remaining, goal[0]))

    cursor.execute("""
        UPDATE spending_limits
        SET remaining = 0
    """)

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({
        "message": f"${total_remaining:.2f} transferred to travel goal"
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

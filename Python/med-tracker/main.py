import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Needed for flash messages

def get_db_connection():
    conn = sqlite3.connect("meds.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS medications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            dosage TEXT NOT NULL,
            med_time TEXT NOT NULL,
            stock INTEGER NOT NULL DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

@app.route("/", methods=["GET", "POST"])
def index():
    conn = get_db_connection()
    if request.method == "POST":
        name = request.form.get("name")
        dosage = request.form.get("dosage")
        med_time = request.form.get("med_time")
        stock = request.form.get("stock", 0)
        if not name or not dosage or not med_time:
            flash("Please fill in all fields.")
        else:
            conn.execute(
                "INSERT INTO medications (name, dosage, med_time, stock) VALUES (?, ?, ?, ?)",
                (name, dosage, med_time, stock)
            )
            conn.commit()
            flash(f"Medication {name} added!")
        return redirect(url_for("index"))
    meds = conn.execute("SELECT * FROM medications").fetchall()
    conn.close()
    return render_template("index.html", meds=meds)

@app.route("/add_stock/<int:med_id>", methods=["POST"])
def add_stock(med_id):
    conn = get_db_connection()
    conn.execute("UPDATE medications SET stock = stock + 1 WHERE id = ?", (med_id,))
    conn.commit()
    conn.close()
    flash("Stock increased.")
    return redirect(url_for("index"))

@app.route("/deduct_stock/<int:med_id>", methods=["POST"])
def deduct_stock(med_id):
    conn = get_db_connection()
    conn.execute("UPDATE medications SET stock = stock - 1 WHERE id = ? AND stock > 0", (med_id,))
    conn.commit()
    conn.close()
    flash("Stock deducted.")
    return redirect(url_for("index"))
@app.route("/delete_med/<int:med_id>", methods=["POST"])

def delete_med(med_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM medications WHERE id = ?", (med_id,))
    conn.commit()
    conn.close()
    flash("Medication removed.")
    return redirect(url_for("index"))

if __name__ == "__main__":
    init_db()
    app.run(debug=True, host="0.0.0.0", port=5000)
from flask import Flask, render_template, request, redirect, session
from models import Hotel, User
import hashlib
import mysql.connector

app = Flask(__name__)
app.config.from_object('config')
app.secret_key = "dev_secret_key"  # move to env later

# ---------------- DB (MySQL) ----------------
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="hotel_app"
)
cursor = db.cursor(dictionary=True)

# ---------------- Sample Data (TEMP) ----------------
hotels = [
    Hotel("Elliot Alderson Executive", 4, "Bangalore", 5, 120),
    Hotel("EAH Deluxe Room", 5, "Bangalore", 5, 200),
    Hotel("EAH Presidential Suite", 6, "Mumbai", 3, 450),
]

users = [
    User("Zubair", 2, 1000),
    User("Elliot", 3, 1200),
    User("Alice", 4, 1100),
]

# ---------------- Public Pages ----------------
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/pricing")
def pricing():
    return render_template("pricing.html")


@app.route("/blogs")
def blogs():
    return render_template("blogs.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


# ---------------- Authentication ----------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = hashlib.sha256(
            request.form["password"].encode()
        ).hexdigest()

        cursor.execute(
            "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
            (name, email, password)
        )
        db.commit()

        return redirect("/login")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = hashlib.sha256(
            request.form["password"].encode()
        ).hexdigest()

        cursor.execute(
            "SELECT * FROM users WHERE email=%s AND password=%s",
            (email, password)
        )
        user = cursor.fetchone()

        if user:
            session["user_id"] = user["id"]
            session["user_name"] = user["name"]
            return redirect("/dashboard")

        return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# ---------------- Protected ----------------
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/login")

    return render_template(
        "dashboard.html",
        user=session["user_name"]
    )


# ---------------- Demo Users Page ----------------
@app.route("/users")
def show_users():
    return render_template("users.html", users=users, hotels=hotels)


# ---------------- Errors ----------------
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)

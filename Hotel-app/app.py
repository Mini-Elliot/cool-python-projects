from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    login_required,
    current_user,
    logout_user,
)
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(30), default="user")  # admin / moderator / user

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if not current_user.is_authenticated:
                return login_manager.unauthorized()
            if current_user.role not in roles:
                flash("You do not have permission to access this page.", "warning")
                return redirect(url_for("dashboard"))
            return f(*args, **kwargs)
        return wrapped
    return decorator


# Replace the decorated function with a normal function that runs inside app context
def create_tables():
    with app.app_context():
        db.create_all()
        # create a default admin if none exists (password: admin)
        if not User.query.filter_by(email="admin@example.com").first():
            admin = User(username="admin", email="admin@example.com", role="admin")
            admin.set_password("admin")
            db.session.add(admin)
            db.session.commit()


@app.route("/")
def index():
    # serve public home page
    return render_template("home.html")


# Public routes (no login required)
@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/pricing")
def pricing():
    return render_template("pricing.html")


@app.route("/blogs")
def blogs():
    # list of public blog entries could be passed here
    return render_template("blogs.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        # ... handle contact form submission (store/email) ...
        flash("Message received. We'll get back to you.", "success")
        return redirect(url_for("contact"))
    return render_template("contact.html")


# Protected routes (require login)
@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")


@app.route("/blog/create", methods=["GET", "POST"])
@login_required
def create_blog():
    if request.method == "POST":
        # ...create blog logic...
        flash("Blog post created.", "success")
        return redirect(url_for("blogs"))
    return render_template("create_blog.html")


@app.route("/booking", methods=["GET", "POST"])
@login_required
def book_hotel():
    if request.method == "POST":
        # ...booking logic...
        flash("Booking confirmed.", "success")
        return redirect(url_for("dashboard"))
    return render_template("booking.html")


@app.route("/manage")
@login_required
@role_required("admin")
def manage_site():
    return render_template("manage.html")


# ---------------- Errors ----------------
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    # ensure DB/tables/default admin exist before serving
    create_tables()
    app.run(debug=True)

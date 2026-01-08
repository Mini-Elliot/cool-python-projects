from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret'
# sqlite DB file placed next to app.py
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(120), nullable=True)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Minimal posts so templates render
posts = [
    {
        "id": 1,
        "slug": "luxury-checklist",
        "title": "5 Tips for a Luxurious Stay",
        "author": "Elliot Alderson",
        "date": "2026-01-01",
        "excerpt": "Discover how to get the most comfort and relaxation during your hotel stay.",
        "image": "https://source.unsplash.com/900x400/?luxury,hotel",
        "content": "<p>Plan ahead, request upgrades, use hotel amenities, and be polite to staff.</p><p>Small touches make a big difference.</p>",
    },
    {
        "id": 2,
        "slug": "top-dining-experiences",
        "title": "Top Dining Experiences",
        "author": "Elliot Alderson",
        "date": "2026-02-10",
        "excerpt": "Explore the best dining options available in luxury hotels.",
        "image": "https://source.unsplash.com/900x400/?hotel,restaurant",
        "content": "<p>From signature tasting menus to in-room dining—discover what makes dining memorable.</p>",
    },
]

# Helper to create admin user
def create_admin(email: str, password: str, name: str = "Admin"):
    if not email or not password:
        return False
    existing = User.query.filter_by(email=email).first()
    if existing:
        return False
    u = User(
        email=email,
        password_hash=generate_password_hash(password),
        name=name,
        is_admin=True,
    )
    db.session.add(u)
    db.session.commit()
    return True

# Routes
@app.route("/")
def index():
    return render_template("index.html", posts=posts)

@app.route("/post/<slug>")
def post_detail(slug):
    post = next((p for p in posts if p["slug"] == slug), None)
    if not post:
        return "Post not found", 404
    return render_template("post.html", post=post)

# Contact/about placeholders to match templates if used
@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        flash("Thanks for your message.", "success")
        return redirect(url_for("contact"))
    return render_template("contact.html")

if __name__ == "__main__":
    # Ensure DB operations run inside the Flask application context
    with app.app_context():
        db.create_all()
        created = create_admin("walker90207@gmail.com", "PasSw0rd!", name="Admin")
        if created:
            print("Admin user created: walker90207@gmail.com")
        else:
            print("Admin user already exists or not created.")
    app.run(debug=True)

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
    render_template_string,  # added
)
from types import SimpleNamespace
from models import hotel_store
import os

ADMIN_EMAIL = "walker90207@gmail.com"
ADMIN_PASSWORD = "PasSw0rd!"

# sample posts used by templates
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


def create_app():
    app = Flask(__name__, template_folder="templates")
    app.secret_key = os.environ.get("EAH_SECRET", "dev-secret")

    # inject current_user and user_role for navbar templates
    @app.context_processor
    def inject_user():
        user = session.get("user")
        if user:
            current = SimpleNamespace(
                is_authenticated=True,
                is_admin=user.get("is_admin", False),
                name=user.get("name", user.get("email")),
                email=user.get("email"),
            )
            role = "admin" if current.is_admin else "user"
        else:
            current = SimpleNamespace(is_authenticated=False, is_admin=False, name=None, email=None)
            role = "guest"
        return {"current_user": current, "user_role": role}

    # Posts listing — expose both 'index' and 'post_list' endpoints
    @app.route("/", endpoint="index")
    @app.route("/posts", endpoint="post_list")
    def index():
        return render_template("index.html", posts=posts)

    @app.route("/post/<slug>")
    def post_detail(slug):
        post = next((p for p in posts if p["slug"] == slug), None)
        if not post:
            return render_template("404.html"), 404
        return render_template("post.html", post=post)

    # About & Contact
    @app.route("/about")
    def about():
        return render_template("about.html")

    @app.route("/contact", methods=["GET", "POST"])
    def contact():
        if request.method == "POST":
            flash("Thanks for your message.", "success")
            return redirect(url_for("contact"))
        return render_template("contact.html")

    # Hotels UI using models.hotel_store
    @app.route("/hotels")
    def hotels():
        return render_template("hotels.html", hotels=hotel_store.list())

    @app.route("/hotels/new", methods=["GET", "POST"])
    def hotel_new():
        if request.method == "POST":
            hotel_store.add(
                request.form.get("name"),
                int(request.form.get("roomAvl") or 0),
                request.form.get("location"),
                float(request.form.get("rating") or 0),
                float(request.form.get("pricePr") or 0),
            )
            flash("Hotel added.", "success")
            return redirect(url_for("hotels"))
        return render_template("hotel_form.html", hotel=None)

    @app.route("/hotels/<int:id>/edit", methods=["GET", "POST"])
    def hotel_edit(id):
        hotel = hotel_store.get(id)
        if not hotel:
            flash("Hotel not found.", "danger")
            return redirect(url_for("hotels"))
        if request.method == "POST":
            hotel_store.update(
                id,
                name=request.form.get("name"),
                roomAvl=int(request.form.get("roomAvl") or 0),
                location=request.form.get("location"),
                rating=float(request.form.get("rating") or 0),
                pricePr=float(request.form.get("pricePr") or 0),
            )
            flash("Hotel updated.", "success")
            return redirect(url_for("hotels"))
        return render_template("hotel_form.html", hotel=hotel)

    @app.route("/hotels/<int:id>/delete", methods=["POST"])
    def hotel_delete(id):
        success = hotel_store.delete(id)
        flash("Hotel deleted." if success else "Hotel not found.", "success" if success else "danger")
        return redirect(url_for("hotels"))

    # Simple game page
    @app.route("/game")
    def game():
        return render_template("game.html")

    # Simple session-based auth (in-memory)
    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            email = request.form.get("email")
            password = request.form.get("password")
            if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
                session["user"] = {"email": email, "name": "Admin", "is_admin": True}
                flash("Logged in as admin.", "success")
                return redirect(url_for("post_list"))
            # accept any other credentials as regular user (demo)
            session["user"] = {"email": email, "name": email.split("@")[0], "is_admin": False}
            flash("Logged in.", "success")
            return redirect(url_for("post_list"))
        return render_template("login.html")

    @app.route("/logout")
    def logout():
        session.pop("user", None)
        flash("Logged out.", "info")
        return redirect(url_for("post_list"))

    # Register route to satisfy url_for('register') used in templates
    @app.route("/register", methods=["GET", "POST"], endpoint="register")
    def register():
        if request.method == "POST":
            email = request.form.get("email")
            name = request.form.get("name") or (email.split("@")[0] if email else "user")
            # demo: no persistence, just create session user
            session["user"] = {"email": email, "name": name, "is_admin": False}
            flash("Registered and logged in.", "success")
            return redirect(url_for("post_list"))
        # Render register.html if available, otherwise fallback simple form
        try:
            return render_template("register.html")
        except Exception:
            fallback = """
            <!doctype html>
            <html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Register</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet"></head>
            <body><main class="container mt-4">
            <h2>Register</h2>
            <form method="post">
              <div class="mb-3"><label class="form-label">Name</label><input name="name" class="form-control"></div>
              <div class="mb-3"><label class="form-label">Email</label><input name="email" type="email" class="form-control" required></div>
              <div class="mb-3"><label class="form-label">Password</label><input name="password" type="password" class="form-control" required></div>
              <button class="btn btn-primary" type="submit">Register</button>
            </form></main>
            </body></html>
            """
            return render_template_string(fallback)

    @app.route("/pricing", endpoint="pricing")
    def pricing():
        # Try to render a dedicated template if it exists, otherwise show a simple fallback page.
        try:
            return render_template("pricing.html")
        except Exception:
            fallback = """
            {% extends "layout.html" %}
            {% block title %}Pricing — EAH{% endblock %}
            {% block content %}
            <section class="py-5">
              <div class="container">
                <h2>Room & Pricing</h2>
                <p class="mb-4">Current room prices (sample data).</p>
                <div class="row">
                  {% for h in hotel_store.list() %}
                  <div class="col-md-4 mb-3">
                    <div class="card h-100">
                      <div class="card-body">
                        <h5 class="card-title">{{ h.name }}</h5>
                        <p class="card-text">Location: {{ h.location }}<br>Rating: {{ h.rating }}</p>
                        <p class="fw-bold">Price: ${{ '%.2f'|format(h.pricePr) }}</p>
                      </div>
                    </div>
                  </div>
                  {% endfor %}
                </div>
              </div>
            </section>
            {% endblock %}
            """
            return render_template_string(fallback, hotel_store=hotel_store)

    # --- Added admin and user pages referenced by templates ---
    @app.route("/admin/dashboard", endpoint="admin_dashboard")
    def admin_dashboard():
        user = session.get("user")
        if not user or not user.get("is_admin"):
            flash("Admin access required.", "danger")
            return redirect(url_for("index"))
        tpl = """
        {% extends "layout.html" %}
        {% block title %}Admin Dashboard — EAH{% endblock %}
        {% block content %}
        <section class="py-5">
          <div class="container">
            <h2>Admin Dashboard</h2>
            <p>Welcome, {{ user.name }}. Use the links to manage the site.</p>
            <ul>
              <li><a href="{{ url_for('admin_posts') }}">Manage Posts</a></li>
              <li><a href="{{ url_for('admin_users') }}">Manage Users</a></li>
              <li><a href="{{ url_for('admin_profile') }}">Profile</a></li>
            </ul>
          </div>
        </section>
        {% endblock %}
        """
        return render_template_string(tpl, user=user)

    @app.route("/admin/posts", endpoint="admin_posts")
    def admin_posts():
        user = session.get("user")
        if not user or not user.get("is_admin"):
            flash("Admin access required.", "danger")
            return redirect(url_for("index"))
        tpl = """
        {% extends "layout.html" %}
        {% block title %}Manage Posts — Admin{% endblock %}
        {% block content %}
        <div class="container py-5"><h2>Manage Posts</h2><p>Post management UI (placeholder).</p></div>
        {% endblock %}
        """
        return render_template_string(tpl)

    @app.route("/admin/users", endpoint="admin_users")
    def admin_users():
        user = session.get("user")
        if not user or not user.get("is_admin"):
            flash("Admin access required.", "danger")
            return redirect(url_for("index"))
        tpl = """
        {% extends "layout.html" %}
        {% block title %}Manage Users — Admin{% endblock %}
        {% block content %}
        <div class="container py-5"><h2>Manage Users</h2><p>User management UI (placeholder).</p></div>
        {% endblock %}
        """
        return render_template_string(tpl)

    @app.route("/admin/profile", endpoint="admin_profile")
    def admin_profile():
        user = session.get("user")
        if not user or not user.get("is_admin"):
            flash("Admin access required.", "danger")
            return redirect(url_for("index"))
        tpl = """
        {% extends "layout.html" %}
        {% block title %}Admin Profile — EAH{% endblock %}
        {% block content %}
        <div class="container py-5">
          <h2>Admin Profile</h2>
          <p>Email: {{ user.email }}</p>
        </div>
        {% endblock %}
        """
        return render_template_string(tpl, user=user)

    @app.route("/dashboard", endpoint="dashboard")
    def dashboard():
        user = session.get("user")
        if not user:
            flash("Please log in.", "warning")
            return redirect(url_for("login"))
        tpl = """
        {% extends "layout.html" %}
        {% block title %}Dashboard — EAH{% endblock %}
        {% block content %}
        <div class="container py-5"><h2>User Dashboard</h2><p>Welcome, {{ user.name }}.</p></div>
        {% endblock %}
        """
        return render_template_string(tpl, user=user)

    @app.route("/profile", endpoint="profile")
    def profile():
        user = session.get("user")
        if not user:
            flash("Please log in.", "warning")
            return redirect(url_for("login"))
        tpl = """
        {% extends "layout.html" %}
        {% block title %}Profile — EAH{% endblock %}
        {% block content %}
        <div class="container py-5"><h2>Profile</h2><p>Email: {{ user.email }}</p></div>
        {% endblock %}
        """
        return render_template_string(tpl, user=user)

    @app.route("/my-posts", endpoint="my_posts")
    def my_posts():
        user = session.get("user")
        if not user:
            flash("Please log in.", "warning")
            return redirect(url_for("login"))
        tpl = """
        {% extends "layout.html" %}
        {% block title %}My Posts — EAH{% endblock %}
        {% block content %}
        <div class="container py-5"><h2>My Posts</h2><p>List of posts authored by {{ user.name }} (placeholder).</p></div>
        {% endblock %}
        """
        return render_template_string(tpl, user=user)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

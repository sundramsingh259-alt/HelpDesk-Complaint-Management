from pathlib import Path
from contextlib import contextmanager
import os
import sqlite3

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)


# ==========================================
# APPLICATION CONFIGURATION
# ==========================================

BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "database.db"

app = Flask(
    __name__,
    template_folder=str(BASE_DIR / "templates"),
    static_folder=str(BASE_DIR / "static")
)

app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY",
    "helpdesk-development-key-change-before-deployment"
)


# ==========================================
# DATABASE CONNECTION
# ==========================================

@contextmanager
def get_db_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")

    try:
        yield connection
        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


# ==========================================
# CREATE DATABASE TABLES
# ==========================================

def create_database():

    with get_db_connection() as connection:

        connection.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'student'
                    CHECK (role IN ('student', 'admin'))
            )
        """)

        connection.execute("""
            CREATE TABLE IF NOT EXISTS complaints (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                category TEXT NOT NULL,
                description TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'Pending'
                    CHECK (
                        status IN (
                            'Pending',
                            'In Progress',
                            'Resolved'
                        )
                    ),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id)
                    REFERENCES users(id)
                    ON DELETE CASCADE
            )
        """)


# ==========================================
# HOME PAGE
# ==========================================

@app.route("/")
def home():

    if session.get("user_id"):
        return redirect(url_for("dashboard"))

    return render_template("index.html")


# ==========================================
# STUDENT REGISTRATION
# ==========================================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not name or not email or not password:
            flash("Please fill in all fields.", "error")
            return redirect(url_for("register"))

        if len(name) > 100:
            flash("Name must be 100 characters or fewer.", "error")
            return redirect(url_for("register"))

        if len(email) > 254 or "@" not in email:
            flash("Please enter a valid email address.", "error")
            return redirect(url_for("register"))

        if len(password) < 8:
            flash("Password must contain at least 8 characters.", "error")
            return redirect(url_for("register"))

        hashed_password = generate_password_hash(password)

        try:

            with get_db_connection() as connection:

                connection.execute(
                    """
                    INSERT INTO users (name, email, password, role)
                    VALUES (?, ?, ?, 'student')
                    """,
                    (name, email, hashed_password)
                )

            flash(
                "Account created successfully! Please log in.",
                "success"
            )

            return redirect(url_for("login"))

        except sqlite3.IntegrityError:

            flash(
                "An account with this email already exists.",
                "error"
            )

            return redirect(url_for("register"))

    return render_template("register.html")


# ==========================================
# LOGIN
# ==========================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not email or not password:
            flash("Please enter your email and password.", "error")
            return redirect(url_for("login"))

        with get_db_connection() as connection:

            user = connection.execute(
                """
                SELECT id, name, email, password, role
                FROM users
                WHERE email = ?
                """,
                (email,)
            ).fetchone()

        if user and check_password_hash(user["password"], password):

            session.clear()

            session["user_id"] = user["id"]
            session["user_name"] = user["name"]
            session["user_role"] = user["role"]

            flash("Login successful!", "success")

            return redirect(url_for("dashboard"))

        flash("Invalid email or password.", "error")

        return redirect(url_for("login"))

    return render_template("login.html")


# ==========================================
# STUDENT DASHBOARD
# ==========================================

@app.route("/dashboard")
def dashboard():

    if not session.get("user_id"):

        flash("Please log in first.", "error")

        return redirect(url_for("login"))

    # Administrators should use their own dashboard.
    if session.get("user_role") == "admin":

        return redirect(url_for("admin_dashboard"))

    # Fetch only the logged-in student's complaints.
    with get_db_connection() as connection:

        complaints = connection.execute(
            """
            SELECT
                id,
                title,
                category,
                description,
                status,
                created_at
            FROM complaints
            WHERE user_id = ?
            ORDER BY id DESC
            """,
            (session["user_id"],)
        ).fetchall()

    return render_template(
        "dashboard.html",
        complaints=complaints,
        user_name=session.get("user_name"),
        user_role=session.get("user_role")
    )


# ==========================================
# SUBMIT A COMPLAINT
# ==========================================

@app.route("/submit_complaint", methods=["POST"])
def submit_complaint():

    if not session.get("user_id"):

        flash("Please log in to submit a complaint.", "error")

        return redirect(url_for("login"))

    if session.get("user_role") != "student":

        flash("Only students can submit complaints.", "error")

        return redirect(url_for("dashboard"))

    title = request.form.get("title", "").strip()
    category = request.form.get("category", "").strip()
    description = request.form.get("description", "").strip()

    allowed_categories = [
        "Infrastructure",
        "Internet",
        "Classroom",
        "Cleanliness",
        "Other"
    ]

    if not title or not category or not description:

        flash("Please fill in all complaint fields.", "error")

        return redirect(url_for("dashboard"))

    if len(title) > 150 or len(description) > 2000:

        flash("Title or description is too long.", "error")

        return redirect(url_for("dashboard"))

    if category not in allowed_categories:

        flash("Please select a valid category.", "error")

        return redirect(url_for("dashboard"))

    with get_db_connection() as connection:

        connection.execute(
            """
            INSERT INTO complaints (
                user_id,
                title,
                category,
                description
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                session["user_id"],
                title,
                category,
                description
            )
        )

    flash(
        "Your complaint has been submitted successfully!",
        "success"
    )

    return redirect(url_for("dashboard"))


# ==========================================
# ADMIN DASHBOARD
# ==========================================

@app.route("/admin")
def admin_dashboard():

    if not session.get("user_id"):

        flash("Please log in first.", "error")

        return redirect(url_for("login"))

    if session.get("user_role") != "admin":

        flash(
            "You are not authorized to access this page.",
            "error"
        )

        return redirect(url_for("dashboard"))

    with get_db_connection() as connection:

        # Fetch all complaints with student details.
        complaints = connection.execute(
            """
            SELECT
                complaints.id,
                complaints.title,
                complaints.category,
                complaints.description,
                complaints.status,
                complaints.created_at,
                users.name,
                users.email
            FROM complaints
            JOIN users
                ON complaints.user_id = users.id
            ORDER BY complaints.id DESC
            """
        ).fetchall()

        # Calculate dashboard statistics.
        total_complaints = connection.execute(
            "SELECT COUNT(*) FROM complaints"
        ).fetchone()[0]

        pending_complaints = connection.execute(
            """
            SELECT COUNT(*)
            FROM complaints
            WHERE status = 'Pending'
            """
        ).fetchone()[0]

        in_progress_complaints = connection.execute(
            """
            SELECT COUNT(*)
            FROM complaints
            WHERE status = 'In Progress'
            """
        ).fetchone()[0]

        resolved_complaints = connection.execute(
            """
            SELECT COUNT(*)
            FROM complaints
            WHERE status = 'Resolved'
            """
        ).fetchone()[0]

    return render_template(
        "admin.html",
        complaints=complaints,
        total_complaints=total_complaints,
        pending_complaints=pending_complaints,
        in_progress_complaints=in_progress_complaints,
        resolved_complaints=resolved_complaints
    )


# ==========================================
# UPDATE COMPLAINT STATUS
# ==========================================

@app.route(
    "/update_status/<int:complaint_id>",
    methods=["POST"]
)
def update_status(complaint_id):

    if not session.get("user_id"):

        flash("Please log in first.", "error")

        return redirect(url_for("login"))

    if session.get("user_role") != "admin":

        flash(
            "Only administrators can update complaint status.",
            "error"
        )

        return redirect(url_for("dashboard"))

    new_status = request.form.get("status", "").strip()

    allowed_statuses = [
        "Pending",
        "In Progress",
        "Resolved"
    ]

    if new_status not in allowed_statuses:

        flash("Please select a valid complaint status.", "error")

        return redirect(url_for("admin_dashboard"))

    with get_db_connection() as connection:

        complaint = connection.execute(
            "SELECT id FROM complaints WHERE id = ?",
            (complaint_id,)
        ).fetchone()

        if complaint is None:

            flash("Complaint not found.", "error")

            return redirect(url_for("admin_dashboard"))

        connection.execute(
            """
            UPDATE complaints
            SET status = ?
            WHERE id = ?
            """,
            (new_status, complaint_id)
        )

    flash("Complaint status updated successfully!", "success")

    return redirect(url_for("admin_dashboard"))


# ==========================================
# LOGOUT
# ==========================================

@app.route("/logout")
def logout():

    session.clear()

    flash("You have been logged out.", "success")

    return redirect(url_for("home"))


# ==========================================
# RUN APPLICATION
# ==========================================

if __name__ == "__main__":

    create_database()

    app.run(debug=True)
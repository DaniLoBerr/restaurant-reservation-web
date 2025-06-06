import sqlite3

from email_validator import validate_email, EmailNotValidError
from flask import (
    flash, Flask, redirect, render_template, request, session, url_for
)
from flask_session import Session
from re import fullmatch
from werkzeug.security import generate_password_hash


# Create Flask app instance with instance-relative config folder
app = Flask(__name__, instance_relative_config=True)

# Load configuration from instance/config.py
app.config.from_pyfile("config.py")

# Initialize server-side session (stored in filesystem)
Session(app)


# Helper functions
def get_db_connection():
    """
    Create and return  a connection to the SQLite database.

    Rows will be returned as dictionaries for easier access by column
    name.
    """
    conn = sqlite3.connect(app.config["DATABASE"])
    conn.row_factory = sqlite3.Row
    return conn


# Routes
@app.route("/")
def index():
    """
    Render the home page.
    """
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """
    Register a new user
    """
    # Forget any existing session
    session.clear()

    if request.method == "POST":

        # Get form data
        username = request.form.get("username")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        phone_number = request.form.get("phone_number")
        email = request.form.get("email")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        error = None

        # Ensure data was submitted
        if not username:
            error = "Username is required."
        elif not first_name:
            error = "First name is required."
        elif not last_name:
            error = "Last name is required."
        elif not phone_number:
            error = "Phone number is required."
        elif not email:
            error = "E-mail is required."
        elif not password:
            error = "Password is required."
        elif not confirmation:
            error = "Password confirmation is required."

        # Validation regex patterns
        regex_username = r"^[a-zA-Z0-9]{6,16}$"
        regex_name = r"^[A-Za-zÀ-ÖØ-öø-ÿ' -]{2,30}$"
        regex_phone = r"^\+?\d[\d\s\-\(\)]{8,}$"
        regex_password = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,30}$"

        # Format validation
        if not error and not fullmatch(regex_username, username):
            error = (
                "Username must be 6-16 characters, letters and numbers only."
            )
        elif not error and (
            not fullmatch(regex_name, first_name)
            or not fullmatch(regex_name, last_name)
        ):
            error = (
                "Names must be 2-30 letters and may include accents, hyphens "
                "or apostrophes."
            )
        elif not error and not fullmatch(regex_phone, phone_number):
            error = "Phone number must be valid."
        elif not error and not fullmatch(regex_password, password):
            error = (
                "Password must be 8-30 characters long and include at least "
                "one uppercase letter, one lowercase letter, one digit, and "
                "one special character."
            )
        elif not error and password != confirmation:
            error = "Password and confirmation must match."
        elif not error:
            try:
                validate_email(email)
            except EmailNotValidError:
                error = "E-mail must be valid."

        # Insert new user into the database
        if error is None:
            try:
                db = get_db_connection()

                # Insert user
                db.execute(
                    "INSERT INTO users(username, first_name, last_name, "
                                        "phone_number,email, hash) "
                    "VALUES(?,?,?,?,?,?)", (
                        username, first_name, last_name, phone_number, email,
                        generate_password_hash(password)
                    )
                )

                db.commit()

            except sqlite3.IntegrityError:
                error = f"User {username} is already registered."

            else:
                # Get the user's ID to store in session
                user = db.execute(
                    "SELECT id FROM users WHERE username = ?", (username,)
                ).fetchone()
                session["user_id"] = user["id"]

                return redirect(url_for("index"))
            
            finally:
                db.close()

        flash(error)

    return render_template("register.html")


# Run the app only when this file is executed directly
if __name__ == "__main__":
    app.run()
from email_validator import validate_email, EmailNotValidError
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from functools import wraps
from re import fullmatch
from werkzeug.security import check_password_hash, generate_password_hash

from restaurant.db import get_db


bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=["GET", "POST"])
def register():
    """Handle user registration via form.
    
    If accessed via GET, render the registration form.
    If accessed via POST, validate the submitted data. If valid,
    insert a new user into the database and redirect to the login
    page. If validation fails, flash an error message and re-render
    the form.
    """
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

        # Get a database connection
        db = get_db()

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
        regex_username = r"^[a-zA-Z0-9_]{3,20}$"
        regex_name = r"^[A-Za-zÀ-ÖØ-öø-ÿ' -]{2,30}$"
        regex_phone = r"^\+?\d[\d\s\-\(\)]{8,}$"
        regex_password = r"^(?=.*[A-Za-z])(?=.*\d).{6,30}$"

        # Format validation
        if not error and not fullmatch(regex_username, username):
            error = (
                "Username must be 3-20 characters, letters, numbers and underscores only."
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
                "Password must be 6-30 characters long and include at least "
                "one letter and one digit."
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
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth/login"))

        flash(error)

    return render_template("auth/register.html")


@bp.route("/login", methods=["GET", "POST"])
def login():
    """Log in a user by validating submitted credentials.

    If accessed via GET, render the login form. If accessed via POST,
    check the submitted username and password against the database.
    If valid, store the user ID in the session and redirect to the
    index page. Otherwise, flash an error message and re-render the
    form.
    """
    if request.method == "POST":

        # Get form data
        username = request.form.get("username")
        password = request.form.get("password")

        error = None

        # Get user data from the database
        db = get_db()
        user = db.execute(
            "SELECT id, hash FROM users WHERE username = ?", (username,)
        ).fetchone()

        # Validate credentials
        if user is None:
            error = "Incorrect username."
        elif not check_password_hash(user["hash"], password):
            error = "Incorrect password."

        # Log in the user
        if error is None:
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for("index"))

        flash(error)

    return render_template("auth/login.html")


@bp.before_app_request
def load_logged_in_user():
    """Load the logged-in user from the database into g.user.
    
    If no user is logged in (no user_id in session), g.user is set to
    None.
    Otherwise, query the database for the user and store the result in
    g.user.
    """
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            "SELECT * FROM users WHERE id = ?", (user_id,)
        ).fetchone
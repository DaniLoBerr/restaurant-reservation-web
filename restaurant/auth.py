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
    """Register a new user."""
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
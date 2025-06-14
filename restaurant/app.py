# Load configuration from instance/config.py
app.config.from_pyfile("config.py")


# Helper functions
def login_required(view):
    """
    Decorate routes to require login.
    """
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if session["user_id"] is None:
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    return wrapped_view


# Routes
@app.route("/")
def index():
    """
    Render the home page.
    """
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Log in a user.
    """
    # Forget any existing session
    session.clear()

    if request.method == "POST":

        # Get form data
        username = request.form.get("username")
        password = request.form.get("password")

        error = None

        # Get user data from the database
        db = get_db_connection()
        user = db.execute(
            "SELECT id, hash FROM users WHERE username = ?", (username,)
        ).fetchone()
        db.close()

        # Validate credentials
        if user is None:
            error = "Incorrect username."
        elif not check_password_hash(user["hash"], password):
            error = "Incorrect password."

        # Log in the user
        if error is None:
            session["user_id"] = user["id"]
            session["username"] = username
            return redirect(url_for("index"))

        flash(error)

    return render_template("login.html")


@app.route("/logout")
def logout():
    """
    Log out a user session
    """
    # Forget any existing session
    session.clear()
    return redirect(url_for("index"))


# Run the app only when this file is executed directly
if __name__ == "__main__":
    app.run()
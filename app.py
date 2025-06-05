import sqlite3

from flask import Flask, render_template
from flask_session import Session


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


# Run the app only when this file is executed directly
if __name__ == "__main__":
    app.run()
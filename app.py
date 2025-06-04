import sqlite3

from flask import Flask, render_template
from flask_session import Session


# Create Flask app instance with relative config folder
app = Flask(__name__, instance_relative_config=True)

# Load configuration from instance/config.py
app.config.from_pyfile("config.py")

# Initialize server-side session (stored in filesystem)
Session(app)


# Define homepage route
@app.route("/")
def index():
    """
    Render the home page.
    """
    
    return render_template("index.html")


# Run the app only if this file is executed directly
if __name__ == "__main__":
    app.run()
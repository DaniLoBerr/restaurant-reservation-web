import os

from flask import Flask, render_template
from flask_session import Session


def create_app():
    """
    Application factory function.
    
    Creates and configures the Flask application instance.
    """

    # Create Flask app instance with relative config folder
    app = Flask(__name__, instance_relative_config=True)

    # Load configuration from instance/config.py
    app.config.from_pyfile("config.py")

    # Initialize server-sode session (stored in filesystem)
    Session(app)

    # Define homepage route
    @app.route("/")
    def index():
        """
        Render the home page.
        """
        
        return render_template("index.html")
    
    return app


# Run the app only if this file is executed directly
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True) # should be False in production
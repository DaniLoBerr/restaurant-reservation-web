import os

from flask import Flask


def create_app(test_config=None):
    """Create and configure the Flask app using the factory pattern."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # A default secret key that should be overriden by instance config
        SECRET_KEY="dev",
        # Store the database in the instance folder
        DATABASE=os.path.join(app.instance_path, "restaurant.sqlite"),
    )

    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Register database initialization with the app instance
    from . import db
    
    db.init_app(app)

    return app
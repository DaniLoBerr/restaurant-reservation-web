import os

# Base directory path
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode during development (should be False in production)
DEBUG = True

# Secret key used for securely signing the session cookie (change in production)
SECRET_KEY = "dev"

# Path to the SQLite3 database
DATABASE = os.path.join(basedir, "restaurant.db")

# Flask-Session configuration
SESSION_PERMANENT = False
SESSION_TYPE = "filesystem"
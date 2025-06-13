import sqlite3
from datetime import datetime

import click
from flask import current_app, g


def get_db():
    """
    Open a new database connection for the current request if needed.
    
    Converts SQLite types to Python native types automatically.
    Return rows of dictionaries for easier access by column name.
    """

    if "db" not in g:
        sqlite3.connect(
            current_app.config["DATABASE"],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None):
    """
    Close the database connection if it was opened during the request.
    
    This function is registered with the app context teardown so that
    the connection is always properly closed after each request.
    """

    db = g.pop("db", None)
    if db is not None:
        db.close()
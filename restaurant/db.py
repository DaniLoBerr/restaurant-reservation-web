import sqlite3
from datetime import datetime

import click
from flask import current_app, g


def get_db():
    """Return a database connection stored in the application context.

    If a connection does not exist yet, create one and set the row
    factory to return rows as dictionaries.
    """
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None):
    """Close the database connection at the end of the request.
    
    Called automatically on application context teardown.
    """
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    """Initialize a new database by executing the schema.sql script."""
    db = get_db()
    with current_app.open_resource("schema.sql") as schema:
        db.executescript(schema.read().decode("utf-8"))


@click.command("init-db")
def init_db_command():
    """Clear existing data and initialize a new database.
    
    The command is registered with the Flask CLI.
    """
    init_db()
    click.echo("Initialized the database.")


def init_app(app):
    """Register dababase functions with the Flask application.
    
    Adds a CLI command to initialize the database.
    Closes the database connection after each request.
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
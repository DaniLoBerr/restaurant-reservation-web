import sqlite3
from datetime import datetime

import click
from flask import current_app, g


def get_db():
    """Open a new database connection for the current request if needed.
    
    Returns rows of dictionaries for easier access by column name.
    """
    if "db" not in g:
        sqlite3.connect(current_app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
    return g.db


def init_db():
    """Initialize a new database by executing the schema.sql script."""
    db = get_db()
    with current_app.open_resource("schema.sql") as schema:
        db.executescript(schema.read.decode("utf-8"))


@click.command("init-db")
def init_db_command():
    """Clear existing data and initialize a new database."""
    init_db()
    click.echo("Initialized the database.")


def close_db(e=None):
    """Close the database connection if it was opened during the request.
    
    This function is registered with the app context teardown so that
    the connection is always properly closed after each request.
    """
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_app(app):
    """Register dababase teardown and CLI command with a given app."""
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
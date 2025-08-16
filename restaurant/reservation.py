from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from restaurant.auth import login_required
from restaurant.db import get_db

bp = Blueprint("reservation", __name__)


@bp.route("/")
def index():
    """Display the main page of the website.
    
    Lists all booked reservations from all users, ordered by date in
    ascending order.
    """
    db = get_db()
    reservations = db.execute(
        "SELECT " \
            "users.username AS 'User' " \
            "reservations.date AS 'Date' " \
            "reservations.party_size AS 'Number of Guests' " \
            "time_slots.start_time AS 'Time' " \
        "FROM reservations " \
        "JOIN users ON users.id = reservations.user_id "
        "JOIN time_slots ON time_slots.id = reservations.slot_id " \
        "ORDER BY reservations.date ASC, time_slots.label ASC"
    ).fetchall()
    return render_template("reservation/index.html", reservations=reservations)

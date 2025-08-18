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
            "users.username, " \
            "reservations.date, " \
            "reservations.party_size, " \
            "time_slots.start_time " \
        "FROM reservations " \
        "JOIN users ON users.id = reservations.user_id "
        "JOIN time_slots ON time_slots.id = reservations.slot_id " \
        "ORDER BY reservations.date ASC, time_slots.label ASC"
    ).fetchall()
    return render_template("reservation/index.html", reservations=reservations)


@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
    if request.method == "POST":
        # Get form data
        date = request.form.get("date")
        time = request.form.get("slot_id")
        party = request.form.get("party_size")
        
        error = None

        # Ensure data was submitted
        if not date:
            error = "Date is required"
        elif not time:
            error = "Time is required"
        elif not party:
            error = "Number of Guests is required"

        # Insert new reservation into the database
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "INSERT INTO reservations(" \
                    "user_id, " \
                    "date, " \
                    "slot_id, " \
                    "party_size, " \
                    "status " \
                    ") " \
                "VALUES(?,?,?,?,?)", (
                    g.user["id"],
                    date,
                    time,
                    party,
                    "confirmed"
                )
            )
            db.commit()
            return redirect(url_for("restaurant.index"))
        
    return render_template("restaurant/create.html")


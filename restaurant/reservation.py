from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from restaurant.auth import login_required
from restaurant.db import get_db

bp = Blueprint("reservation", __name__)


@bp.route("/")
def index():
    """Display the main page of the website.
    
    Lists all booked reservations from all users, ordered by date and 
    time in ascending order.
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
        "WHERE status IS 'confirmed' "
        "ORDER BY reservations.date ASC, time_slots.label ASC"
    ).fetchall()
    return render_template("reservation/index.html", reservations=reservations)


@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
    """Handle reservation creation requests.
    
    - GET: Render a form to create a new reservation.
    - POST: Validate the submitted data and, if valid, insert the
    reservation into the database. Redirects to the reservation list
    upon success, otherwise re-renders the form with an error message.
    """
    if request.method == "POST":
        # Get form data
        date = request.form.get("date")
        time = request.form.get("time")
        party = request.form.get("party")
        
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
                    int(party),
                    "confirmed"
                )
            )
            db.commit()
            return redirect(url_for("reservation.read"))
        
    return render_template("reservation/create.html")


@bp.route("/my-reservations")
@login_required
def read():
    """Display all reservations of the authenticated user.
    
    Lists all booked reservations from the currently logged-in user and
    renders them in the "reservation/read.html" template, ordered by
    date and time in ascending order.
    """
    reservations = get_db().execute(
        "SELECT " \
            "reservations.id, " \
            "reservations.date, " \
            "reservations.party_size, " \
            "reservations.created_at, " \
            "time_slots.start_time " \
        "FROM reservations " \
        "JOIN users ON users.id = reservations.user_id " \
        "JOIN time_slots ON time_slots.id = reservations.slot_id " \
        "WHERE user_id = ? " \
        "AND status IS 'confirmed' "
        "ORDER BY reservations.date ASC, time_slots.label ASC",
        (g.user["id"],)
    ).fetchall()
    return render_template("reservation/read.html", reservations=reservations)


@bp.route("/<int:id>/update", methods=("POST",))
@login_required
def update(id):
    """Update an existing reservation.
    
    This route can be accessed in two ways:
        - When the user clicks the "Edit" button for one of their
        reservations on the "My Reservations" page. In this case, it
        receives the reservation id and displays the update form.
        - When the update form is submitted. The input data is
        validated, and if correct, the reservation details are
        updated in the database.
    
    :param id: The id number of the Reservation in the database.
    :type id: int
    """
    if request.form.get("confirmation"):
        # Get form data
        date = request.form.get("date")
        time = request.form.get("time")
        party = request.form.get("party")
        
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
                "UPDATE reservations " \
                "SET "
                    "date = ?, " \
                    "slot_id = ?, " \
                    "party_size = ? " \
                    "WHERE id = ? ",
                (date, time, int(party), id)
            )
            db.commit()
            return redirect(url_for("reservation.read"))

    return render_template("reservation/update.html", reservation_id=id)


@bp.route("/<int:id>/delete", methods=("POST",))
@login_required
def delete(id):
    """Mark a reservation as "cancelled".
    
    This view receives a reservation id, updates its status to
    "cancelled" in the database, commits the change, and redirects the
    user to the "My Reservations" page.
    """
    db = get_db()
    db.execute(
        "UPDATE reservations SET status = 'cancelled' WHERE id = ?", (id,)
    )
    db.commit()
    return redirect(url_for("reservation.read"))


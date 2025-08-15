from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from restaurant.auth import login_required
from restaurant.db import get_db

bp = Blueprint("reservation", __name__)
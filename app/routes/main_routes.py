from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from app.models.event import Event
from app.models.assignment import Assignment

main_bp = Blueprint("main", __name__)


@main_bp.route("/dashboard")
@login_required
def dashboard():

    if current_user.is_admin:
        return redirect(url_for("admin.dashboard"))

    events = current_user.events
    poem_status = {}

    for event in events:
        assignment = Assignment.query.filter_by(
            event_id=event.id, giver_id=current_user.id
        ).first()

        poem_status[event.id] = bool(
            assignment and assignment.poem and assignment.poem.strip()
        )

    return render_template("dashboard.html", events=events, poem_status=poem_status)

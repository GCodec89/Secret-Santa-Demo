from flask import Blueprint, render_template, abort
from app.models.event import Event

event_bp = Blueprint("event", __name__)


@event_bp.route("/events/<int:event_id>")
def event_detail(event_id):
    event = Event.query.get(event_id)
    if not event:
        abort(404, "Event not found.")

    assignments = list(event.assignments)

    return render_template("event_detail.html", event=event, assignments=assignments)

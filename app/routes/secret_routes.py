from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

from app import db
from app.models.assignment import Assignment
from app.models.event import Event

secret_bp = Blueprint("secret", __name__)


# ---------- VIEW MY SECRET SANTA ----------
@secret_bp.route("/my-secret/<int:event_id>")
@login_required
def my_secret(event_id):

    if current_user.is_admin:
        return render_template(
            "my_secret_santa.html", message="Admin doesn't participate in the draw."
        )

    event = Event.query.get_or_404(event_id)

    if current_user not in event.participants:
        return render_template(
            "my_secret_santa.html", message="You are not participating in this event."
        )

    assignment = Assignment.query.filter_by(
        event_id=event.id, giver_id=current_user.id
    ).first()

    if not assignment:
        return render_template(
            "my_secret_santa.html",
            message="The draw has not yet taken place for this event.",
        )

    return render_template("my_secret_santa.html", receiver=assignment.receiver)


# ---------- VIEW FINISHED EVENT + EDIT MY POEM ----------
@secret_bp.route("/event/<int:event_id>/view", methods=["GET", "POST"])
@login_required
def view_event(event_id):
    event = Event.query.get_or_404(event_id)

    if not event.is_finished:
        flash("This event is not over yet.", "danger")
        return redirect(url_for("main.dashboard"))

    if current_user not in event.participants:
        flash("You are not participating in this event.", "danger")
        return redirect(url_for("main.dashboard"))

    assignments = Assignment.query.filter_by(event_id=event.id).all()

    if request.method == "POST":
        for assignment in assignments:
            if assignment.giver_id == current_user.id:
                poem_text = request.form.get(f"poem_{assignment.id}")
                assignment.poem = poem_text.strip() if poem_text else None
        db.session.commit()
        flash("Your poem has been saved!", "success")
        return redirect(url_for("secret.view_event", event_id=event.id))

    return render_template("poems_view.html", event=event, assignments=assignments)

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required

from app import db
from app.models.event import Event
from app.models.assignment import Assignment
from app.models.user import User

from app.utils import admin_required
from app.utils.secret_santa import assign_secret_santa
from app.utils.email_utils import (
    send_draw_email,
    send_finish_event_email,
)

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


# ---------- DASHBOARD ----------
@admin_bp.route("/")
@login_required
@admin_required
def dashboard():
    return render_template("admin_dashboard.html")


# ---------- MANAGE PARTICIPANTS ----------
@admin_bp.route("/users", methods=["GET", "POST"])
@login_required
@admin_required
def manage_users():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        if not name or not email or not password:
            flash("Name, email and password are required.", "danger")
            return redirect(url_for("admin.manage_users"))

        if User.query.filter_by(email=email).first():
            flash("User already exists.", "danger")
            return redirect(url_for("admin.manage_users"))

        user = User(name=name, email=email)
        user.set_password(password)
        user.is_admin_flag = False

        db.session.add(user)
        db.session.commit()

        flash("Participant created successfully!", "success")
        return redirect(url_for("admin.manage_users"))

    users = User.query.filter_by(is_admin_flag=False).all()
    return render_template("admin_manage_users.html", users=users)


# ---------- EDIT PARTICIPANT ----------
@admin_bp.route("/users/<int:user_id>/edit", methods=["GET", "POST"])
@login_required
@admin_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)

    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        if not name or not email:
            flash("Name and email are required.", "danger")
            return redirect(url_for("admin.edit_user", user_id=user.id))

        if User.query.filter(User.email == email, User.id != user.id).first():
            flash("Email already in use by another user.", "danger")
            return redirect(url_for("admin.edit_user", user_id=user.id))

        user.name = name
        user.email = email

        if password:
            user.set_password(password)

        db.session.commit()
        flash("Participant updated successfully!", "success")
        return redirect(url_for("admin.manage_users"))

    return render_template("admin_edit_user.html", user=user)


# ---------- DELETE PARTICIPANT ----------
@admin_bp.route("/users/<int:user_id>/delete", methods=["POST"])
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)

    if user.is_admin_flag:
        flash("Cannot delete admin user.", "danger")
        return redirect(url_for("admin.manage_users"))

    assignments_count = Assignment.query.filter(
        (Assignment.giver_id == user.id) | (Assignment.receiver_id == user.id)
    ).count()

    if assignments_count > 0:
        flash(
            "Cannot delete participant because they were involved in an event.",
            "danger",
        )
        return redirect(url_for("admin.manage_users"))

    if len(user.events) > 0:
        flash(
            "Cannot delete participant because they are part of an active event.",
            "danger",
        )
        return redirect(url_for("admin.manage_users"))

    db.session.delete(user)
    db.session.commit()

    flash(f"Participant {user.name} deleted successfully!", "success")
    return redirect(url_for("admin.manage_users"))


# ---------- LIST EVENTS ----------
@admin_bp.route("/events")
@login_required
@admin_required
def events():
    events = Event.query.order_by(Event.year.desc()).all()
    return render_template("admin_events.html", events=events)


# ---------- CREATE EVENT ----------
@admin_bp.route("/events/create", methods=["GET", "POST"])
@login_required
@admin_required
def create_event():
    users = User.query.filter_by(is_admin_flag=False).all()

    if request.method == "POST":
        name = request.form.get("name")
        year_str = request.form.get("year")
        selected_users = request.form.getlist("participants")

        if not name or not year_str:
            flash("Name and year are required.", "danger")
            return redirect(url_for("admin.create_event"))

        if len(selected_users) < 2:
            flash("Select at least 2 participants.", "danger")
            return redirect(url_for("admin.create_event"))

        try:
            year = int(year_str)
        except ValueError:
            flash("Year must be a number.", "danger")
            return redirect(url_for("admin.create_event"))

        event = Event(name=name, year=year)
        db.session.add(event)
        db.session.commit()

        for user_id in selected_users:
            user = User.query.get(int(user_id))
            if user:
                event.participants.append(user)

        db.session.commit()
        flash("Event created successfully!", "success")
        return redirect(url_for("admin.events"))

    return render_template("admin_create_event.html", users=users)


# ---------- EDIT EVENT ----------
@admin_bp.route("/events/<int:event_id>/edit", methods=["GET", "POST"])
@login_required
@admin_required
def edit_event(event_id):
    event = Event.query.get_or_404(event_id)
    users = User.query.filter_by(is_admin_flag=False).all()

    if request.method == "POST":
        name = request.form.get("name")
        year_str = request.form.get("year")
        selected_ids = request.form.getlist("participants")

        if not name or not year_str:
            flash("Name and year are required.", "danger")
            return redirect(url_for("admin.edit_event", event_id=event.id))

        try:
            year = int(year_str)
        except ValueError:
            flash("Year must be a number.", "danger")
            return redirect(url_for("admin.edit_event", event_id=event.id))

        event.name = name
        event.year = year
        event.participants = User.query.filter(User.id.in_(selected_ids)).all()

        db.session.commit()
        flash("Event updated successfully!", "success")
        return redirect(url_for("admin.events"))

    return render_template("admin_edit_event.html", event=event, users=users)


# ---------- DELETE EVENT ----------
@admin_bp.route("/events/<int:event_id>/delete", methods=["POST"])
@login_required
@admin_required
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    db.session.delete(event)
    db.session.commit()

    flash("Event deleted successfully!", "success")
    return redirect(url_for("admin.events"))


# ---------- DRAW SECRET SANTA ----------
@admin_bp.route("/events/<int:event_id>/draw", methods=["POST"])
@login_required
@admin_required
def draw_event(event_id):
    event = Event.query.get_or_404(event_id)

    if len(event.participants) < 2:
        flash("Not enough participants to perform draw.", "danger")
        return redirect(url_for("admin.events"))

    try:
        assign_secret_santa(event)

        assignments = Assignment.query.filter_by(event_id=event.id).all()

        for assignment in assignments:
            send_draw_email(
                user=assignment.giver,
                event=event,
                assigned_user=assignment.receiver,
            )

        flash(
            "Secret Santa draw completed successfully! Emails sent 🎄",
            "success",
        )

    except Exception as e:
        flash(str(e), "danger")

    return redirect(url_for("admin.events"))


# ---------- FINISH EVENT ----------
@admin_bp.route("/events/<int:event_id>/finish", methods=["POST"])
@login_required
@admin_required
def finish_event(event_id):
    event = Event.query.get_or_404(event_id)

    if not event.is_draw_done:
        flash("Cannot finish event before draw.", "danger")
        return redirect(url_for("admin.events"))

    if event.is_finished:
        flash("Event already finished.", "warning")
        return redirect(url_for("admin.events"))

    event.is_finished = True
    db.session.commit()

    for user in event.participants:
        send_finish_event_email(user=user, event=event)

    flash(
        f"Event '{event.name}' finished. Participants notified by email ✉️",
        "success",
    )
    return redirect(url_for("admin.events"))


# ---------- VIEW RESULTS + POEMS ----------
@admin_bp.route("/events/<int:event_id>/view")
@login_required
@admin_required
def view_event_results(event_id):
    event = Event.query.get_or_404(event_id)

    if not event.is_finished:
        flash("Event not finished yet.", "danger")
        return redirect(url_for("admin.events"))

    assignments = Assignment.query.filter_by(event_id=event.id).all()
    return render_template(
        "admin_assignments.html",
        event=event,
        assignments=assignments,
    )


# ---------- SAVE POEMS ----------
@admin_bp.route("/events/<int:event_id>/save_poems", methods=["POST"])
@login_required
@admin_required
def save_poems(event_id):
    event = Event.query.get_or_404(event_id)
    assignments = event.assignments.all()

    for assignment in assignments:
        poem_text = request.form.get(f"poem_{assignment.id}")
        if poem_text is not None:
            assignment.poem = poem_text.strip()

    db.session.commit()
    flash("Poems updated successfully!", "success")
    return redirect(url_for("admin.view_event_results", event_id=event.id))

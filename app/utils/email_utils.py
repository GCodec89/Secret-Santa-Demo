from flask import current_app


def send_draw_email(user, event, assigned_user):
    print(
        f"[DEBUG] {user.email} would receive an email: you'll be giving a gift to {assigned_user.name}"
    )


def send_finish_event_email(user, event):
    print(f"[DEBUG] {user.email} would receive an email: Event {event.name} finished")

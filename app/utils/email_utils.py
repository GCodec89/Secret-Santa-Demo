from flask_mail import Message
from flask import current_app, url_for
from app import mail


def send_draw_email(user, event, assigned_user):

    login_url = "http://127.0.0.1:5000/login"

    subject = f"🎄 {event.name}"

    body = f"""
Hi {user.name},

The drawing for the "{event.name}" has already taken place 🎁

👉 You're going to give the gift to:
{assigned_user.name}

Don't forget to write your poem ✍️

🔐 Login:
Email: {user.email}
Password: (a tua password habitual)

Access here:
{login_url}

Have fun!
🎄 Secret Santa
"""

    msg = Message(
        subject=subject,
        recipients=[user.email],
        body=body,
        sender=current_app.config["MAIL_USERNAME"],
    )

    mail.send(msg)


def send_finish_event_email(user, event):

    event_url = f"http://127.0.0.1:5000/event/{event.id}/view"

    subject = f"🎭 {event.name} — Event finished"

    body = f"""
Hi {user.name},

The event "{event.name}" came to an edn 🎉

It's time to submit your poem ✍️

👉 Access here:
{event_url}

Thank you!
🎄 Secret Santa
"""

    msg = Message(
        subject=subject,
        recipients=[user.email],
        body=body,
        sender=current_app.config["MAIL_USERNAME"],
    )

    mail.send(msg)

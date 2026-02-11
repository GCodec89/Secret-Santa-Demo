# Secret Santa Demo 🎄

🔗 **Live Demo:** https://secret-santa-demo.onrender.com/

A simple **Flask** web application for running a Secret Santa event.  
Built with clean architecture, role-based access control, and deployed on **Render** for live demonstration.

---

## Demo Access

- **Email:** `admin@test.com`  
- **Password:** `123456`

> The admin user is created automatically on first run.

---

## Features

- Admin dashboard
- Participant management (CRUD)
- Event creation and editing
- Secret Santa draw logic (no self-assignments)
- Event completion phase
- Poem submission system
- Email simulation (logged instead of sent)

---

## Important Notes

- This is a **presentation/demo version**.
- Real emails are **not sent** — all notifications are printed to the server logs.
- The database runs on Render and persists between sessions.

---

## Tech Stack

- Python 3
- Flask
- SQLAlchemy
- Flask-Login
- Bootstrap
- Gunicorn
- Render (deployment)

---

## How It Works

1. Admin creates participants.
2. Admin creates an event and selects participants.
3. Click **Draw** → Secret Santa assignments are generated.
4. Click **Finish Event** → Event enters poem submission phase.
5. Results can be viewed in the admin panel.

---

## Author

Developed by Gonçalo Codeço  
GitHub: https://github.com/GCodec89

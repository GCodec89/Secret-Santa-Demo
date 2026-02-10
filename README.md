# Secret Santa Demo 🎄

A simple **Flask** app for running a Secret Santa event, ready for demo on **Render**.  
Login as admin to create participants, create events, run the draw, and view results.

---

## Demo Login

- **Email:** `admin@test.com`  
- **Password:** `123456`

> The admin user is created automatically on first run.

---

## Important Notes

- This demo is **presentation-only**: no real emails are sent.  
  All messages are printed in the server logs instead.
- Database changes are persisted on Render in `app.db` but are **not tracked in Git**.

---

## Deploy & Run on Render

When using Render, you **do not need to install dependencies or run the server manually**.  
Render handles everything automatically.

---

## How It Works

- Admin creates participants and events.
- Click Draw → Secret Santa assignments are generated.
- Click Finish Event → Event is marked as completed, poems can be submitted.
- Emails are simulated in the logs (debug mode).
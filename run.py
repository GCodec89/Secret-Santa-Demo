import os
from flask import render_template
from flask_login import login_required

from app import create_app

app = create_app()


@app.route("/")
@login_required
def dashboard():
    return render_template("dashboard.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

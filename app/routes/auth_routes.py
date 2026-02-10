from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user

from app.models.user import User


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):

            login_user(user)

            if user.is_admin:
                return redirect(url_for("admin.dashboard"))
            else:
                return redirect(url_for("main.dashboard"))

        flash("Invalid email or password", "danger")

    if current_user.is_authenticated:

        if current_user.is_admin:
            return redirect(url_for("admin.dashboard"))
        else:
            return redirect(url_for("main.dashboard"))

    return render_template("login.html")


@auth_bp.route("/logout")
@login_required
def logout():

    logout_user()
    flash("You have been logged out.", "info")

    return redirect(url_for("auth.login"))

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
import os

# ------------------- EXTENSIONS -------------------
db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()


# ------------------- ADMIN -------------------
def create_default_admin():
    from app.models.user import User
    from sqlalchemy.exc import OperationalError

    try:
        admin_exists = User.query.filter_by(is_admin_flag=True).first()
        if not admin_exists:
            admin = User(name="Admin", email="admin@test.com")
            admin.set_password("123456")
            admin.is_admin_flag = True
            db.session.add(admin)
            db.session.commit()
            print("✅ Default admin created: admin@test.com / 123456")
        else:
            print("ℹ️ Admin already exists")
    except OperationalError:
        print("⚠️ Database not ready yet — admin creation skipped")


# ------------------- FACTORY -------------------
def create_app():
    app = Flask(__name__)
    app.config.update(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev-secret-key"),
        SQLALCHEMY_DATABASE_URI=os.environ.get("DATABASE_URL", "sqlite:///app.db"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        MAIL_SERVER=os.environ.get("MAIL_SERVER", "localhost"),
        MAIL_PORT=int(os.environ.get("MAIL_PORT", 25)),
        MAIL_USE_TLS=True,
        MAIL_USERNAME=os.environ.get("MAIL_USERNAME"),
        MAIL_PASSWORD=os.environ.get("MAIL_PASSWORD"),
        MAIL_DEFAULT_SENDER=os.environ.get("MAIL_DEFAULT_SENDER"),
    )

    # ---------- INIT EXTENSIONS ----------
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    login_manager.login_view = "auth.login"

    # ---------- IMPORT MODELS ----------
    from app.models.user import User
    from app.models.event import Event
    from app.models.assignment import Assignment

    # ---------- BLUEPRINTS ----------
    from app.routes.auth_routes import auth_bp
    from app.routes.admin_routes import admin_bp
    from app.routes.main_routes import main_bp
    from app.routes.secret_routes import secret_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(secret_bp)

    # ---------- CREATE DATABASE & ADMIN ----------
    with app.app_context():
        db.create_all()
        create_default_admin()

    return app

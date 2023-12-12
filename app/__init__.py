import os

from flask import Flask
from werkzeug.security import generate_password_hash

from .extensions import db, login_manager
from .models import User
from app.master_routes import bp as master_bp


def create_app():
    app = Flask(__name__)
    app.register_blueprint(master_bp)
    app.config.from_object(os.environ.get("APP_SETTINGS", "config.DevelopmentConfig"))

    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        db.create_all()
        if os.environ.get("APP_SETTINGS", "config.DevelopmentConfig") == "config.DevelopmentConfig":
            add_test_user()
            print("Test user added")
        return app


def add_test_user():
    if User.query.filter_by(email='test@example.com').first() is None:
        test_user = User(email='test@example.com', password=generate_password_hash('password'))
        db.session.add(test_user)
        db.session.commit()

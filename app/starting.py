from flask import Flask


def create_app():
    app = Flask(__name__)

    with app.app_context():
        from routes import main_routes

        app.register_blueprint(main_routes)

        return app

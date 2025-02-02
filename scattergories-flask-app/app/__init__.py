from flask import Flask
from .routes import main as main_routes
from .models import db
import os

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('instance.config.Config')  # Load the configuration from config.py

    db.init_app(app)

    app.register_blueprint(main_routes)

    with app.app_context():
        db.create_all()

    return app
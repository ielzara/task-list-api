from flask import Flask
from flask_cors import CORS
from .db import db, migrate
from .models import task, goal
from .routes.task_routes import bp as tasks_bp
from .routes.goal_routes import bp as goals_bp
import os
from dotenv import load_dotenv

load_dotenv(override=True)


def create_app(config=None):
    app = Flask(__name__)
    CORS(app)

    app.config["CORS_HEADERS"] = "Content-Type"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    database_url = os.environ.get("SQLALCHEMY_DATABASE_URI")

    app.config["SQLALCHEMY_DATABASE_URI"] = database_url

    if config:
        # Merge `config` into the app's configuration
        # to override the app's default settings for testing
        app.config.update(config)

    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints here
    app.register_blueprint(tasks_bp)
    app.register_blueprint(goals_bp)

    return app

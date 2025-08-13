# app/main.py
from flask import Flask
from app.core.config import Config
from app.core.extensions import db, jwt, migrate
from app.api.routes import api_bp
import logging
import os


def create_app():
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(Config)

    # Initialize Flask extensions
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    # Logging to file + console
    if not os.path.exists("logs"):
        os.mkdir("logs")
    logging.basicConfig(
        filename='logs/app.log',
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s'
    )
    logging.getLogger().addHandler(logging.StreamHandler())

    # Register Blueprints
    app.register_blueprint(api_bp, url_prefix="/api")

    @app.before_first_request
    def create_tables():
        from app.models.request_log import RequestLog
        db.create_all()

    return app

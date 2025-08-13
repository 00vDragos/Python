from flask import Flask
from flask_cors import CORS
from app.core.config import Config
from app.core.extensions import db, jwt, migrate
from app.api.routes import api_bp
import logging
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    from flask_cors import CORS

    CORS(
        app,
        resources={r"/api/*": {"origins": "*"}},
        supports_credentials=True,
        allow_headers=["Content-Type", "Authorization"],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    )

    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    if not os.path.exists("logs"):
        os.mkdir("logs")
    logging.basicConfig(
        filename='logs/app.log',
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s'
    )
    logging.getLogger().addHandler(logging.StreamHandler())

    app.register_blueprint(api_bp, url_prefix="/api")
    return app

from main import create_app
from app.core.extensions import db
from flask import Flask
from flask_cors import CORS
# from app.models.request_log import RequestLog

app = create_app()

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)




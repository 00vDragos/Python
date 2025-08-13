import sys
import os
sys.path.append(os.path.abspath("."))
import main
app = main.create_app()
from app.models.user import User
from app.core.extensions import db

import main
app = main.create_app()

with app.app_context():
    user = User.query.filter_by(email="test@gmail.com").first()
    if user:
        print(f"User gasit: {user.email}")
        print(f"Parola hashata: {user.password_hash}")
    else:
        print("Userul nu exista.")

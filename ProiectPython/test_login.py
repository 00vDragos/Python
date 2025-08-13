import sys
import os
sys.path.append(os.path.abspath("."))

import main
from app.models.user import User
from app.core.extensions import db

app = main.create_app()

with app.app_context():
    user = User.query.filter_by(email="test@gmail.com").first()
    if user:
        print(f"User gasit: {user.email}")
        if user.check_password("parola"):
            print("Parola este corecta.")
        else:
            print("Parola este gresita.")
    else:
        print("Userul nu exista.")

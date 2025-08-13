import os

db_path = os.path.join("instance", "mathapi.db")

if os.path.exists(db_path):
    try:
        os.remove(db_path)
        print("Baza de date a fost stearsa.")
    except Exception as e:
        print("Eroare la stergere:", e)
else:
    print("ℹBaza de date nu exista deja.")

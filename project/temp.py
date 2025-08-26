from project.config import app, db

with app.app_context():
    # db.drop_all()    # Optional: removes existing tables
    db.create_all()  # ✅ Creates tables based on your models

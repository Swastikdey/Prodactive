from project.config import db
from datetime import datetime
from flask_login import UserMixin
class Reminders(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    task_name = db.Column(db.String(200), unique = False, nullable = False)
    time = db.Column(db.Time)
    date = db.Column(db.Date)
    completed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


    def to_json(self):
        return {
            "id":self.id,
            "taskName" : self.task_name,
            "time":self.time.strftime("%H:%M"),
            "date":self.date.isoformat(),
            "completed":self.completed,
        }
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200), unique = False, nullable = False)
    phone = db.Column(db.String(10), unique = True, nullable = False)
    email = db.Column(db.String(100), unique = True, nullable = False)
    is_phone_verified = db.Column(db.Boolean, default = False)
    is_email_verified = db.Column(db.Boolean, default = False)
    password_hash = db.Column(db.String(128), nullable=False)
    reminders = db.relationship('Reminders', backref='user', lazy=True)


from flask_login import UserMixin
from datetime import datetime

from .db import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.Integer)
    name = db.Column(db.String(150))
    surname = db.Column(db.String(150))
    city = db.Column(db.String(170))
    country = db.Column(db.String(60))
    date_created = db.Column(db.DateTime, default=datetime.now)

    # gen AI
    scans = db.relationship(
        "Scan",
        backref="user",
        cascade="all, delete-orphan"
    )

class Scan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    url = db.Column(db.String(2048), nullable=False)
    scan_date = db.Column(db.DateTime, default=datetime.now)
    result = db.Column(db.Text, nullable=False)

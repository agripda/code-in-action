# models.py
# This defines the database model for hotels.

from app import db

class Hotel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    city = db.Column(db.String(100))
    street = db.Column(db.String(100))
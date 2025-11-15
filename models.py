from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Destination(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    location = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)
    image = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f'<Destination {self.name}>'

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    destination_id = db.Column(db.Integer, db.ForeignKey('destination.id'), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(40), nullable=True)
    num_people = db.Column(db.Integer, nullable=False, default=1)
    date = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(30), nullable=False, default='Booked')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    destination = db.relationship('Destination', backref=db.backref('bookings', lazy=True))

    def __repr__(self):
        return f'<Booking {self.name} -> {self.destination_id}>'

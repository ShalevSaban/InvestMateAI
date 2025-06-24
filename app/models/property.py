from app import db
import uuid
from datetime import datetime


class Property(db.Model):
    __tablename__ = 'properties'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    agent_id = db.Column(db.String(36), db.ForeignKey('agents.id'), nullable=False)

    city = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Numeric, nullable=False)
    yield_percent = db.Column(db.Numeric)
    property_type = db.Column(db.Enum('apartment', 'house', 'vacation', name='property_type_enum'))
    rooms = db.Column(db.Integer)
    floor = db.Column(db.Integer)
    description = db.Column(db.Text)
    rental_estimate = db.Column(db.Numeric)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Property in {self.city}, {self.price}>"

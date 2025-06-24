from app import db
import uuid
from datetime import datetime


class Agent(db.Model):
    __tablename__ = 'agents'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    full_name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    properties = db.relationship('Property', backref='agent', lazy=True, cascade="all, delete")
    conversations = db.relationship('Conversation', backref='agent', lazy=True, cascade="all, delete")

    def __repr__(self):
        return f"<Agent {self.email}>"

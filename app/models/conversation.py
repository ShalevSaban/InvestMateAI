from app import db
import uuid
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSONB


class Conversation(db.Model):
    __tablename__ = 'conversations'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    agent_id = db.Column(db.String(36), db.ForeignKey('agents.id'), nullable=False)
    client_identifier = db.Column(db.String(100), nullable=False)
    chat_history = db.Column(JSONB, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Conversation with {self.client_identifier}>"

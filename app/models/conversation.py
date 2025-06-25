from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from app.database import Base
import uuid
from datetime import datetime


class Conversation(Base):
    __tablename__ = 'conversations'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    agent_id = Column(String(36), ForeignKey('agents.id'), nullable=False)
    client_identifier = Column(String(100), nullable=False)
    chat_history = Column(JSONB, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Conversation with {self.client_identifier}>"

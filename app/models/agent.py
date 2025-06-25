from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
import uuid
from datetime import datetime


class Agent(Base):
    __tablename__ = 'agents'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    full_name = Column(String(100), nullable=False)
    phone_number = Column(String(20), nullable=True)
    email = Column(String(100), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    properties = relationship('Property', backref='agent', lazy=True, cascade="all, delete")
    conversations = relationship('Conversation', backref='agent', lazy=True, cascade="all, delete")

    def __repr__(self):
        return f"<Agent {self.email}>"

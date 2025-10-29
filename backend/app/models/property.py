from sqlalchemy import Column, String, Integer, DateTime, Numeric, Text, Enum, ForeignKey
from app.database import Base
import uuid
from datetime import datetime


class Property(Base):
    __tablename__ = 'properties'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    agent_id = Column(String(36), ForeignKey('agents.id', ondelete='CASCADE'), nullable=False)

    city = Column(String(100), nullable=False)
    address = Column(String(200), nullable=False)
    price = Column(Numeric, nullable=False)
    yield_percent = Column(Numeric, nullable=True)
    property_type = Column(Enum('apartment', 'house', 'vacation', name='property_type_enum'))
    rooms = Column(Integer)
    floor = Column(Integer)
    description = Column(Text)
    rental_estimate = Column(Numeric, nullable=True)
    image_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Property in {self.city}, {self.price}>"

from sqlalchemy import Column, Text
from app.database import Base


class CachedCriteria(Base):
    __tablename__ = "cached_criteria"

    question = Column(Text, primary_key=True)
    criteria_json = Column(Text, nullable=False)

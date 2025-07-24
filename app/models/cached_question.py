from sqlalchemy import Column, Text, String
from app.database import Base


class CachedQuestion(Base):
    __tablename__ = "cached_questions"

    question = Column(Text, primary_key=True)
    answer = Column(Text, nullable=False)
    language = Column(String, nullable=True)

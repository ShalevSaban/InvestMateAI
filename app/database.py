from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/realestate")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def create_tables():
    from app.models.agent import Agent
    from app.models.property import Property
    from app.models.conversation import Conversation

    Base.metadata.create_all(bind=engine)

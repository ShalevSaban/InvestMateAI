# app/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

#DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/realestate")
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# ✅ פונקציית get_db לשימוש ב־Depends
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ✅ יצירת טבלאות (אם צריך להריץ ידנית)
def create_tables():
    from app.models.agent import Agent
    from app.models.property import Property


    Base.metadata.create_all(bind=engine)

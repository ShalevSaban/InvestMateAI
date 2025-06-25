from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# קבלת URL למסד הנתונים מתוך משתני סביבה או ברירת מחדל
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/realestate")

# יצירת engine ללא connect_args מיותרים (כי לא מדובר ב-SQLite)
engine = create_engine(DATABASE_URL)

# Session ל-DB, מחובר ל-engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# בסיס למודלים של SQLAlchemy
Base = declarative_base()


# יצירת הטבלאות בעת הפעלת האפליקציה (startup)
def create_tables():
    from app.models.agent import Agent
    from app.models.property import Property
    from app.models.conversation import Conversation

    Base.metadata.create_all(bind=engine)

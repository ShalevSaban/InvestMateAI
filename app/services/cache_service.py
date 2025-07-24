from sqlalchemy.orm import Session
from app.models.cached_question import CachedQuestion


def get_cached_answer(db: Session, question: str) -> str | None:
    cached = db.query(CachedQuestion).filter(CachedQuestion.question == question).first()
    return cached.answer if cached else None


def store_answer_in_cache(db: Session, question: str, answer: str, language: str | None = None):
    db.add(CachedQuestion(question=question, answer=answer, language=language))
    db.commit()

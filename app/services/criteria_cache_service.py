import json
from sqlalchemy.orm import Session
from app.models.cached_criteria import CachedCriteria


def get_cached_criteria(question: str, db: Session) -> dict | None:
    cached = db.query(CachedCriteria).filter_by(question=question).first()
    return json.loads(cached.criteria_json) if cached else None


def save_criteria_to_cache(question: str, criteria: dict, db: Session):
    json_data = json.dumps(criteria, ensure_ascii=False)
    db.add(CachedCriteria(question=question, criteria_json=json_data))
    db.commit()

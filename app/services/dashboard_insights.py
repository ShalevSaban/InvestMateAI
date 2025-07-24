from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from uuid import UUID
from app.models import Message, Conversation, Property
from app.services.gpt_service import GPTService
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.insight_log import InsightLog
import json


def get_faqs(agent_id: UUID, db: Session):
    results = (
        db.query(Message.content, func.count(Message.id).label("count"))
            .join(Conversation)
            .filter(Conversation.agent_id == agent_id)
            .filter(Message.role == "user")
            .group_by(Message.content)
            .order_by(desc("count"))
            .limit(5)
            .all()
    )
    return [{"question": r[0], "count": r[1]} for r in results]


def get_peak_hours(agent_id: UUID, db: Session):
    results = (
        db.query(func.extract("hour", Message.created_at).label("hour"), func.count(Message.id))
            .join(Conversation)
            .filter(Conversation.agent_id == agent_id)
            .filter(Message.role == "user")
            .group_by("hour")
            .order_by("hour")
            .all()
    )

    def to_local_hour(utc_hour):
        return (int(utc_hour) + 3) % 24  # UTC+3 (Israel)

    return [{"hour": to_local_hour(r[0]), "count": r[1]} for r in results]


def get_popular_properties(agent_id: UUID, db: Session):
    results = (
        db.query(Property.address, func.count(Message.id).label("mentions"))
            .select_from(Conversation)
            .join(Message, Message.conversation_id == Conversation.id)
            .join(Property, Property.agent_id == Conversation.agent_id)
            .filter(Conversation.agent_id == agent_id)
            .filter(Message.role == "user")
            .filter(Message.content.ilike(func.concat('%', Property.address, '%')))
            .group_by(Property.address)
            .order_by(desc("mentions"))
            .limit(5)
            .all()
    )
    return [{"address": r[0], "mentions": r[1]} for r in results]


def get_strategy_suggestions(agent_id: UUID, db: Session):
    messages = (
        db.query(Message.content)
            .join(Conversation)
            .filter(Conversation.agent_id == agent_id)
            .filter(Message.role == "user")
            .order_by(desc(Message.created_at))
            .limit(50)
            .all()
    )
    text = "\n".join([m.content for m in messages])
    return GPTService.generate_gpt_insights(agent_id, text)


def get_cached_gpt_insight(agent_id: str, db: Session) -> dict | None:
    today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    log = (
        db.query(InsightLog)
        .filter(
            InsightLog.agent_id == str(agent_id),
            InsightLog.created_at >= today
        )
        .first()
    )
    if log:
        return json.loads(log.insight_result)
    return None


def save_gpt_insight(agent_id: str, result: dict, db: Session):
    json_result = json.dumps(result, ensure_ascii=False)
    log = InsightLog(agent_id=str(agent_id), insight_result=json_result)
    db.add(log)
    db.commit()

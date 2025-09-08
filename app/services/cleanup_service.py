# services/cleanup_service.py
from datetime import datetime, timedelta, timezone
from uuid import UUID

from sqlalchemy import and_
from sqlalchemy.orm import Session
from app.models import Agent, Conversation, Message


def keep_last_10_conversations_per_agent(db: Session):
    agents = db.query(Agent).all()
    total_deleted_convs = 0

    for agent in agents:
        convs = (
            db.query(Conversation)
                .filter(Conversation.agent_id == agent.id)
                .order_by(Conversation.created_at.desc())
                .all()
        )
        to_delete = convs[10:]
        to_delete_ids = [conv.id for conv in to_delete]

        if to_delete_ids:
            db.query(Message).filter(Message.conversation_id.in_(to_delete_ids)).delete(synchronize_session=False)
            db.query(Conversation).filter(Conversation.id.in_(to_delete_ids)).delete(synchronize_session=False)
            total_deleted_convs += len(to_delete_ids)

    db.commit()
    return {"deleted_conversations": total_deleted_convs}


def delete_old_conversations_for_agent(db: Session, agent_id: str, days: int = 2) -> dict:
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    print("cutoff_date",cutoff_date)
    # מציאת שיחות ישנות של הסוכן
    old_conversations = (
        db.query(Conversation)
            .filter(and_(
            Conversation.agent_id == agent_id,
            Conversation.created_at < cutoff_date
        ))
            .all()
    )

    old_conversation_ids = [conv.id for conv in old_conversations]
    print("ids",old_conversation_ids)

    if not old_conversation_ids:
        return {
            "deleted_messages": 0,
            "deleted_conversations": 0,
            "cutoff_date": cutoff_date.isoformat()
        }

    # מחיקת ההודעות תחילה (foreign key constraint)
    deleted_messages = (
        db.query(Message)
            .filter(Message.conversation_id.in_(old_conversation_ids))
            .delete(synchronize_session=False)
    )

    # מחיקת השיחות
    deleted_conversations = (
        db.query(Conversation)
            .filter(Conversation.id.in_(old_conversation_ids))
            .delete(synchronize_session=False)
    )

    db.commit()

    return {
        "deleted_messages": deleted_messages,
        "deleted_conversations": deleted_conversations,
        "cutoff_date": cutoff_date.isoformat()
    }

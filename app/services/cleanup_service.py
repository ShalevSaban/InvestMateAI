# services/cleanup_service.py

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

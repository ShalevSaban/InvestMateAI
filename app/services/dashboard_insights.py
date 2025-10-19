from sqlalchemy.orm import Session
from uuid import UUID
from app.services.conversation_cache import ConversationCache
from app.services.gpt_service import GPTService
from app.services.insight_cache import InsightCache
from datetime import datetime
import json


def get_faqs(agent_id: UUID, db: Session):
    """Get FAQs from Redis conversations"""
    return ConversationCache.get_faqs(str(agent_id), limit=5)


def get_peak_hours(agent_id: UUID, db: Session):
    """Get peak hours from Redis conversations"""
    return ConversationCache.get_peak_hours(str(agent_id))


def get_popular_properties(agent_id: UUID, db: Session):
    """Get popular properties from Redis conversations"""
    return ConversationCache.get_popular_properties(str(agent_id), db, limit=5)
    # OR simpler:
    # return ConversationCache.get_popular_properties(str(agent_id), db)


def get_strategy_suggestions(agent_id: UUID, db: Session):
    """Get GPT insights from Redis conversations"""
    conversations = ConversationCache.get_agent_conversations(str(agent_id), limit=50)

    # Extract all user messages
    all_messages = []
    for conv in conversations:
        for msg in conv.get("messages", []):
            if msg["role"] == "user":
                all_messages.append(msg["content"])

    text = "\n".join(all_messages)

    if not text.strip():
        return {
            "summary": "לא נמצאו שיחות לניתוח",
            "frequent_needs": [],
            "potential_opportunities": [],
            "recommended_actions": []
        }

    return GPTService.generate_gpt_insights(str(agent_id), text)


# def get_cached_gpt_insight(agent_id: str, db: Session) -> dict | None:
#     """Get cached GPT insight (still uses PostgreSQL for now)"""
#     today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
#     log = (
#         db.query(InsightLog)
#             .filter(
#             InsightLog.agent_id == str(agent_id),
#             InsightLog.created_at >= today
#         )
#             .first()
#     )
#     if log:
#         return json.loads(log.insight_result)
#     return None
#
#
# def save_gpt_insight(agent_id: str, result: dict, db: Session):
#     """Save GPT insight (still uses PostgreSQL for now)"""
#     json_result = json.dumps(result, ensure_ascii=False)
#     log = InsightLog(agent_id=str(agent_id), insight_result=json_result)
#     db.add(log)
#     db.commit()

def get_cached_gpt_insight(agent_id: str, db: Session) -> dict | None:
    """Get cached GPT insight from Redis (not PostgreSQL anymore!)"""
    return InsightCache.get_cached_insight(agent_id)


def save_gpt_insight(agent_id: str, result: dict, db: Session):
    """Save GPT insight to Redis"""
    InsightCache.save_insight(agent_id, result)


def get_conversation_stats(agent_id: UUID) -> dict:
    """Get conversation statistics from Redis"""
    return ConversationCache.get_conversation_stats(str(agent_id))

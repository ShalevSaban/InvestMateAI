from datetime import datetime
from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID

# Updated import
from app.services.cache_service import CacheService
from app.services.gpt_service import GPTService, detect_language, build_response_message
from app.services.property_service import search_properties_by_criteria
from app.models import Conversation, Message, Agent
from app.schemas.property import PropertyOut
from app.services.conversation_cache import ConversationCache
from uuid import uuid4


def process_chat_question(question: str, db: Session, agent_id: Optional[UUID] = None):
    question = question.strip()
    lang = detect_language(question)
    print("User ask question:\n", question)

    agent = db.query(Agent).filter(Agent.id == str(agent_id)).first() if agent_id else None

    # Get criteria (already using Redis cache)
    criteria = CacheService.get_search_criteria(question)
    if not criteria:
        criteria = GPTService.extract_search_criteria(question)
        CacheService.save_search_criteria(question, criteria)

    filters = {
        k: v for k, v in criteria.items()
        if k in {
            "city", "address", "min_price", "max_price", "min_rooms", "max_rooms",
            "min_floor", "max_floor", "floor", "property_type",
            "rental_estimate_max", "yield_percent", "description_filters"
        }
    }
    if agent:
        filters["agent_id"] = str(agent.id)

    properties = search_properties_by_criteria(filters, db)
    reply = build_response_message(criteria, properties, lang)
    print("response: ",reply)

    # Save to Redis instead of PostgreSQL
    conversation_id = str(uuid4())


    if agent:
            ConversationCache.save_message(str(agent.id), conversation_id, "user", question)
            #ConversationCache.save_message(str(agent.id), conversation_id, "assistant", reply)

    for prop in properties:
        ConversationCache.track_property_mention(str(agent.id), prop.address)

    return {
        "conversation_id": conversation_id,
        "message": reply,
        "filters": filters,
        "results": [PropertyOut.model_validate(p).model_dump() for p in properties],
        "source": "redis_cache"
    }
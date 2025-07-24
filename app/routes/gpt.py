from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Conversation, Message, Agent
from app.services.gpt_service import GPTService, detect_language, build_response_message
from app.services.property_service import search_properties_by_criteria
from app.schemas.property import PropertyOut
from app.services.cache_service import get_cached_answer, store_answer_in_cache


router = APIRouter(prefix="/gpt", tags=["GPT"])

from typing import Optional
from uuid import UUID


@router.post("/chat")
def chat_with_gpt(
    question: str = Body(..., embed=True),
    agent_id: Optional[UUID] = Body(None, embed=True),
    db: Session = Depends(get_db),
):
    question = question.strip()
    lang = detect_language(question)

    agent = db.query(Agent).filter(Agent.id == str(agent_id)).first() if agent_id else None

    # 🔍 חישוב criteria ו־filters (בכל מקרה)
    criteria = GPTService.extract_search_criteria(question)
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

    # 🧠 בדיקה אם יש תשובה מה־cache
    cached = get_cached_answer(db, question)
    if cached:
        print("✅ Retrieved answer from cache")
        return {
            "conversation_id": None,
            "message": cached,
            "filters": filters,
            "results": [PropertyOut.model_validate(p) for p in properties],
            "source": "cache"
        }

    # 🗨 יצירת שיחה חדשה
    conversation = Conversation(agent_id=agent.id if agent else None)
    db.add(conversation)
    db.commit()
    db.refresh(conversation)

    user_msg = Message(content=question, role="user", conversation_id=conversation.id)
    db.add(user_msg)

    reply = build_response_message(criteria, properties, lang)

    assistant_msg = Message(content=reply, role="assistant", conversation_id=conversation.id)
    db.add(assistant_msg)
    db.commit()

    store_answer_in_cache(db, question, reply, lang)
    return {
        "conversation_id": str(conversation.id),
        "message": reply,
        "filters": filters,
        "results": [PropertyOut.model_validate(p) for p in properties],
        "source": "gpt"
    }

from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Conversation, Message, Agent
from app.services.gpt_service import GPTService, detect_language, build_response_message
from app.services.property_service import search_properties_by_criteria
from app.schemas.property import PropertyOut
from app.services.criteria_cache_service import get_cached_criteria, save_criteria_to_cache

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

    criteria = get_cached_criteria(question, db)
    if not criteria:
        print("save cache")
        criteria = GPTService.extract_search_criteria(question)
        save_criteria_to_cache(question, criteria, db)

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

    conversation = Conversation(agent_id=agent.id if agent else None)
    db.add(conversation)
    db.commit()
    db.refresh(conversation)

    user_msg = Message(content=question, role="user", conversation_id=conversation.id)
    db.add(user_msg)

    # 🧠 בניית תשובה בזמן ריצה לפי תוצאות חיפוש
    reply = build_response_message(criteria, properties, lang)

    assistant_msg = Message(content=reply, role="assistant", conversation_id=conversation.id)
    db.add(assistant_msg)
    db.commit()

    return {
        "conversation_id": str(conversation.id),
        "message": reply,
        "filters": filters,
        "results": [PropertyOut.model_validate(p) for p in properties],
        "source": "criteria_cache"
    }

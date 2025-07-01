from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.gpt_service import GPTService, detect_language, build_response_message
from app.services.property_service import search_properties_by_criteria

router = APIRouter(prefix="/gpt", tags=["GPT"])


@router.post("/chat")
def chat_with_gpt(question: str = Body(..., embed=True), db: Session = Depends(get_db)):
    question = question.strip()
    lang = detect_language(question)

    # הפקת קריטריונים
    criteria = GPTService.extract_search_criteria(question)

    # סינון קריטריונים רלוונטיים
    filters = {
        k: v for k, v in criteria.items()
        if k in {
            "city", "address", "min_price", "max_price", "min_rooms", "max_rooms",
            "min_floor", "max_floor", "floor", "property_type",
            "rental_estimate_max", "yield_percent"
        }
    }

    # חיפוש נכסים
    properties = search_properties_by_criteria(filters, db)

    # יצירת תגובה טבעית
    reply = build_response_message(criteria, properties, lang)

    # החזרת תשובה
    return {
        "message": reply,
        "filters": filters,
        "results": properties
    }

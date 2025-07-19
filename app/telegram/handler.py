from app.services.gpt_service import GPTService, detect_language, build_response_message
from app.services.property_service import search_properties_by_criteria
from sqlalchemy.orm import Session


def handle_telegram_message(message: str, db: Session, agent_id=None) -> str:
    message = message.strip()
    lang = detect_language(message)

    # הפעלת GPT לצורך חילוץ קריטריונים
    criteria = GPTService.extract_search_criteria(message)

    # חיפוש במסד הנתונים לפי הקריטריונים
    results = search_properties_by_criteria(criteria, db, agent_id)

    # בניית תשובה בהתאם לשפה
    reply = build_response_message(criteria, results, lang)

    return reply

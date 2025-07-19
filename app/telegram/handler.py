from app.services.gpt_service import GPTService, detect_language, build_response_message
from app.services.property_service import search_properties_by_criteria
from app.database import get_db
from sqlalchemy.orm import Session


def handle_telegram_message(message: str, db: Session, agent_id=None) -> str:
    message = message.strip()
    lang = detect_language(message)

    gpt_output = GPTService().run(message, lang)
    properties = search_properties_by_criteria(gpt_output, db, agent_id)
    reply = build_response_message(properties, lang)
    return reply

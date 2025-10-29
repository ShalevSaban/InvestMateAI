from app.services.chat_service import process_chat_question
from app.services.gpt_service import GPTService, detect_language, build_response_message
from app.services.property_service import search_properties_by_criteria
from sqlalchemy.orm import Session


def handle_telegram_message(message: str, db: Session, agent_id=None) -> str:
    return process_chat_question(message, db, agent_id)

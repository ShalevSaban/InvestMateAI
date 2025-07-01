# from sqlalchemy.orm import Session
# from app.models.conversation import Conversation, Message
# from uuid import UUID
# from openai import ChatCompletion
# from app.services.gpt_service import build_gpt_prompt
# from app.services.gpt_service import GPTService
# from app.services.property_service import search_properties_by_criteria
#
#
# def create_conversation(db: Session) -> Conversation:
#     conversation = Conversation()
#     db.add(conversation)
#     db.commit()
#     db.refresh(conversation)
#     return conversation
#
#
# def save_message(db: Session, conversation_id: UUID, role: str, content: str) -> Message:
#     message = Message(
#         conversation_id=conversation_id,
#         role=role,
#         content=content
#     )
#     db.add(message)
#     db.commit()
#     db.refresh(message)
#     return message
#
#
# def chat_with_gpt(question: str, db: Session, conversation_id: UUID = None):
#     # Start or get conversation
#     conversation = db.query(Conversation).filter_by(id=conversation_id).first() if conversation_id else create_conversation(db)
#
#     # Save user message
#     save_message(db, conversation.id, "user", question)
#
#     # Rebuild prompt from past messages (for now just last 5)
#     past_messages = db.query(Message).filter_by(conversation_id=conversation.id).order_by(Message.created_at).limit(5).all()
#     prompt = build_gpt_prompt(past_messages)
#
#     # GPT call
#     response = ChatCompletion.create(
#         model="gpt-4",
#         messages=prompt
#     )
#     assistant_reply = response.choices[0].message["content"]
#
#     # Save assistant reply
#     save_message(db, conversation.id, "assistant", assistant_reply)
#
#     return {
#         "conversation_id": conversation.id,
#         "reply": assistant_reply
#     }

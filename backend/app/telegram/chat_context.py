# app/telegram/chat_context.py

chat_to_agent = {}  # chat_id (int) -> agent_id (UUID str)


def set_agent_for_chat(chat_id: int, agent_id: str):
    chat_to_agent[chat_id] = agent_id


def get_agent_for_chat(chat_id: int) -> str | None:
    return chat_to_agent.get(chat_id)

from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.telegram.handler import handle_telegram_message
from app.telegram.chat_context import set_agent_for_chat, get_agent_for_chat
import httpx
import os

router = APIRouter(prefix="/telegram", tags=["Telegram"])
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")


@router.post("/webhook")
async def telegram_webhook(req: Request, db: Session = Depends(get_db)):
    data = await req.json()
    message = data.get("message", {})
    text = message.get("text", "").strip()
    chat_id = message.get("chat", {}).get("id")

    if not text or not chat_id:
        return {"ok": False, "reason": "Missing data"}

    # אם זה /start <agent_id>
    if text.startswith("/start"):
        parts = text.split()
        if len(parts) > 1:
            agent_id = parts[1]
            set_agent_for_chat(chat_id, agent_id)

            # שלח הודעת ברוך הבא
            async with httpx.AsyncClient() as client:
                await client.post(
                    f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
                    json={
                        "chat_id": chat_id,
                        "text": f"✅ התחברת לסוכן בהצלחה! אתה יכול עכשיו לשאול שאלה חופשית."
                    }
                )
            return {"ok": True}

    # אחרת – חפש את agent_id מההקשר
    agent_id = get_agent_for_chat(chat_id)
    response_text = handle_telegram_message(text, db, agent_id)

    async with httpx.AsyncClient() as client:
        await client.post(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
            json={"chat_id": chat_id, "text": response_text}
        )

    return {"ok": True}

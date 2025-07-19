from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.telegram.handler import handle_telegram_message
import httpx
import os

router = APIRouter(prefix="/telegram", tags=["Telegram"])

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")


@router.post("/webhook")
async def telegram_webhook(req: Request, db: Session = Depends(get_db)):
    data = await req.json()
    message = data.get("message", {})
    text = message.get("text")
    chat = message.get("chat", {})
    chat_id = chat.get("id")

    if not text or not chat_id:
        return {"ok": False, "reason": "Missing text or chat_id"}

    # בעתיד נוכל לחלץ agent_id מ־deep link או /start
    response_text = handle_telegram_message(text, db)

    async with httpx.AsyncClient() as client:
        await client.post(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
            json={"chat_id": chat_id, "text": response_text}
        )

    return {"ok": True}

from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.telegram.handler import handle_telegram_message
from app.telegram.chat_context import set_agent_for_chat, get_agent_for_chat
import httpx
import os

router = APIRouter(prefix="/telegram", tags=["Telegram"])
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
DOMAIN = os.getenv("DOMAIN", "localhost:8000")


@router.post("/webhook")
async def telegram_webhook(req: Request, db: Session = Depends(get_db)):
    data = await req.json()
    message = data.get("message", {})
    text = message.get("text", "").strip()
    chat_id = message.get("chat", {}).get("id")

    if not text or not chat_id:
        return {"ok": False, "reason": "Missing data"}

    async with httpx.AsyncClient() as client:

        # אם זה /start <agent_id>
        if text.startswith("/start"):
            parts = text.split()
            if len(parts) > 1:
                agent_id = parts[1]
                set_agent_for_chat(chat_id, agent_id)

                # שלח הודעת ברוך הבא
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

        # קבלת התוצאה המלאה (dict) מ־process_chat_question
        result = handle_telegram_message(text, db, agent_id)

        # שולח הודעה ראשית עם התקציר
        await client.post(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
            json={"chat_id": chat_id, "text": result["message"]}
        )

        # עבור כל נכס – שולח הודעה נפרדת עם פרטים
        for p in result.get("results", []):
            details = (
                f"📍 {p['city']}, {p['address']}\n"
                f"💰 Price: {p.get('price', 'N/A')}\n"
                f"🛏 Rooms: {p.get('rooms', 'N/A')} | 🏢 Floor: {p.get('floor', 'N/A')}\n"
                f"🏷 Type: {p.get('property_type', 'N/A')}\n"
                f"🔁 Yield: {p.get('yield_percent', 'N/A')}%\n"
                f"🪙 Rent: {p.get('rental_estimate', 'N/A')}₪\n"
                f"📄 {p.get('description', 'No description.')}\n"
                f"👤 Agent: {p.get('agent', {}).get('full_name', 'N/A')}\n"
                f"📞 Phone: {p.get('agent', {}).get('phone_number', 'N/A')}"
            )


            # שולח טקסט מפורט
            await client.post(
                f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
                json={"chat_id": chat_id, "text": details}
            )

            # ניסיון לשלוח גם תמונה (אם קיים image-url)
            try:
                img_res = await client.get(f"http://{DOMAIN}/properties/{p['id']}/image-url")
                if img_res.status_code == 200:
                    img_data = img_res.json()
                    image_url = img_data.get("image_url")
                    if image_url:
                        await client.post(
                            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto",
                            json={"chat_id": chat_id, "photo": image_url}
                        )
            except Exception as e:
                print(f"Failed to fetch/send image for property {p['id']}: {e}")

    return {"ok": True}

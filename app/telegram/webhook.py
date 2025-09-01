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

                # הודעת ברוך הבא מקצועית דו-לשונית
                welcome_message = """🏡 Welcome to InvestMateAI!
Your smart real estate assistant is ready to help you find the perfect property using natural language search.

📍 **Available Properties:**
Our database features properties from top agents in: Tel Aviv, Herzliya, Netanya, Givatayim, and Ramat Gan.

🔍 **How to Search:**
Simply ask about any property criteria you're looking for - location, price range, rooms, amenities, or specific features.

💡 **Example Query:**
"Show me an apartment in Ramat Gan with over 2% yield near a metro station"

**Pro Tips:**
• Use natural language - ask as you would speak
• Specify amenities like "pool," "balcony," or "parking"
• Set price ranges, room counts, or yield requirements
• Ask about specific neighborhoods or streets

Start exploring your next investment opportunity! 🚀

---

🏡 ברוכים הבאים ל-InvestMateAI!
העוזר החכם שלכם לנדל"ן מוכן לעזור לכם למצוא את הנכס המושלם באמצעות חיפוש בשפה טבעית.

📍 **נכסים זמינים:**
מאגר הנכסים שלנו כולל נכסים מסוכנים מובילים בערים: תל אביב, הרצליה, נתניה, גבעתיים ורמת גן.

🔍 **איך לחפש:**
פשוט שאלו על כל קריטריון שאתם מחפשים - מיקום, טווח מחירים, חדרים, שירותים או מאפיינים ספציפיים.

💡 **דוגמה לשאלה:**
"תראה לי דירה ברמת גן עם תשואה מעל 2% ליד תחנת מטרו"

**טיפים מקצועיים:**
• השתמשו בשפה טבעית - שאלו כמו שאתם מדברים
• ציינו שירותים כמו "בריכה", "מרפסת" או "חניה"
• קבעו טווחי מחירים, מספר חדרים או דרישות תשואה
• שאלו על שכונות או רחובות ספציפיים

התחילו לחקור את ההשקעה הבאה שלכם! 🚀"""

                await client.post(
                    f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
                    json={
                        "chat_id": chat_id,
                        "text": welcome_message
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
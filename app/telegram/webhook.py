from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.telegram.handler import handle_telegram_message
from app.telegram.chat_context import set_agent_for_chat, get_agent_for_chat
from app.models.agent import Agent
from app.models.property import Property
import httpx
import os

router = APIRouter(prefix="/telegram", tags=["Telegram"])
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
DOMAIN = os.getenv("DOMAIN", "localhost:8000")


async def send_agent_selection_menu(client, chat_id, db: Session):
    """שולח רשימה של סוכנים זמינים לבחירה"""
    agents = db.query(Agent).all()

    if not agents:
        await client.post(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
            json={
                "chat_id": chat_id,
                "text": "❌ אין סוכנים זמינים כרגע. אנא נסה שוב מאוחר יותר."
            }
        )
        return

    # יצירת כפתורים inline לבחירת סוכן
    buttons = []
    for agent in agents:
        property_count = db.query(Property).filter(Property.agent_id == agent.id).count()
        buttons.append([{
            "text": f"{agent.full_name} ({property_count} נכסים)",
            "callback_data": f"select_agent:{agent.id}"
        }])

    # הוספת אופציה לראות את כל הנכסים
    buttons.append([{
        "text": "🏠 כל הנכסים (כל הסוכנים)",
        "callback_data": "select_agent:all"
    }])

    await client.post(
        f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
        json={
            "chat_id": chat_id,
            "text": "🏡 ברוכים הבאים ל-InvestMateAI!\n\n"
                    "אנא בחרו סוכן נדל\"ן מהרשימה למטה כדי לראות את הנכסים שלו:",
            "reply_markup": {
                "inline_keyboard": buttons
            }
        }
    )


async def send_agent_welcome_message(client, chat_id, db: Session, agent_id: str):
    """שולח הודעת ברכה עם פרטי הסוכן והנכסים"""
    if agent_id == "all":
        # כל הנכסים
        properties = db.query(Property).all()
        agent_name = "כל הסוכנים"
        welcome_text = f"🎉 נבחרו כל הנכסים!\n\n"
    else:
        # סוכן ספציפי
        agent = db.query(Agent).filter(Agent.id == agent_id).first()
        if not agent:
            await client.post(
                f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
                json={
                    "chat_id": chat_id,
                    "text": "❌ סוכן לא נמצא. אנא התחילו מחדש עם /start"
                }
            )
            return

        properties = db.query(Property).filter(Property.agent_id == agent_id).all()
        agent_name = agent.full_name
        welcome_text = f"🎉 התחברתם לסוכן {agent_name}!\n\n"

    # סטטיסטיקות על הנכסים
    if properties:
        cities = list(set([p.city for p in properties]))
        avg_price = sum([float(p.price or 0) for p in properties]) / len(properties)

        welcome_text += f"📊 **סטטיסטיקות:**\n"
        welcome_text += f"🏠 {len(properties)} נכסים זמינים\n"
        welcome_text += f"🏙️ ערים: {', '.join(cities[:3])}" + (
            f" ועוד {len(cities) - 3}" if len(cities) > 3 else "") + "\n"
        welcome_text += f"💰 מחיר ממוצע: ₪{avg_price:,.0f}\n\n"

        welcome_text += "💬 **איך לחפש:**\n"
        welcome_text += "• \"דירות בתל אביב עד 5 מיליון\"\n"
        welcome_text += "• \"בית עם בריכה בהרצליה\"\n"
        welcome_text += "• \"3 חדרים עם מרפסת\"\n"
        welcome_text += "• \"דירה עם תשואה מעל 2 אחוז\"\n\n"

        welcome_text += "🔍 פשוט כתבו מה אתם מחפשים ואני אמצא עבורכם!\n\n"

        welcome_text += "Attention! This is the Hebrew welcome version, but you can also search properties in English using free language 🌍."

    else:
        welcome_text += f"😔 לא נמצאו נכסים עבור {agent_name}.\n"
        welcome_text += "אנא בחרו סוכן אחר או נסו שוב מאוחר יותר."

    await client.post(
        f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
        json={
            "chat_id": chat_id,
            "text": welcome_text,
            "parse_mode": "Markdown"
        }
    )


@router.post("/webhook")
async def telegram_webhook(req: Request, db: Session = Depends(get_db)):
    data = await req.json()

    # בדיקת callback query (לחיצה על כפתור)
    callback_query = data.get("callback_query")
    if callback_query:
        return await handle_callback_query(callback_query, db)

    message = data.get("message", {})
    text = message.get("text", "").strip()
    chat_id = message.get("chat", {}).get("id")

    if not text or not chat_id:
        return {"ok": False, "reason": "Missing data"}

    async with httpx.AsyncClient() as client:
        print(f"🔵 Received message: '{text}' from chat_id: {chat_id}")  # לוג לבדיקה

        # אם זה /start
        if text.startswith("/start"):
            parts = text.split()
            if len(parts) > 1:
                # /start עם agent_id ישירות (מלינק)
                agent_id = parts[1]
                set_agent_for_chat(chat_id, agent_id)
                await send_agent_welcome_message(client, chat_id, db, agent_id)
                return {"ok": True}
            else:
                # /start רגיל - הצג תפריט בחירת סוכן
                await send_agent_selection_menu(client, chat_id, db)
                return {"ok": True}

        # בדיקה אם יש סוכן מוגדר
        agent_id = get_agent_for_chat(chat_id)
        if not agent_id:
            # אין סוכן מוגדר - הצג תפריט בחירה
            await send_agent_selection_menu(client, chat_id, db)
            return {"ok": True}

        # טיפול בהודעות חיפוש רגילות
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


async def handle_callback_query(callback_query, db: Session):
    """טיפול בלחיצות על כפתורים"""
    query_id = callback_query["id"]
    chat_id = callback_query["message"]["chat"]["id"]
    data = callback_query["data"]

    async with httpx.AsyncClient() as client:
        if data.startswith("select_agent:"):
            agent_id = data.split(":")[1]

            # שמירת הסוכן שנבחר
            set_agent_for_chat(chat_id, agent_id)

            # מחיקת התפריט הישן
            await client.post(
                f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/editMessageReplyMarkup",
                json={
                    "chat_id": chat_id,
                    "message_id": callback_query["message"]["message_id"],
                    "reply_markup": {"inline_keyboard": []}
                }
            )

            # שליחת הודעת ברכה עם הדרכה
            await send_agent_welcome_message(client, chat_id, db, agent_id)

            # אישור ל-Telegram שהcallback טופל
            await client.post(
                f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/answerCallbackQuery",
                json={"callback_query_id": query_id, "text": "✅ סוכן נבחר!"}
            )

    return {"ok": True}
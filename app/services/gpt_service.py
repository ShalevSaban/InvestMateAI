import os
import openai
import json
import re
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


class GPTService:
    @staticmethod
    def extract_search_criteria(question: str) -> dict:
        prompt = f"""
You are a real estate assistant. A user asked: "{question}"

Extract a JSON object with the following keys:
- city (string or null)
- address (string or null)
- min_price (number or null)
- max_price (number or null)
- min_rooms (minimum rooms if mentioned)
- max_rooms (maximum rooms if mentioned)
- min_floor (minimum floor if mentioned)
- max_floor (maximum floor if mentioned)
- property_type (string: "apartment", "house", etc. or null)
- rental_estimate_max (number or null) → for monthly rent filter
- yield_percent (minimum or average yield percent)

Output must be valid JSON only. Do not explain anything.
If the question is in Hebrew, translate internally and extract in English.

If the user says "שכירות", "מחיר שכירות", or "שכר דירה" rent,rent price, rental price – always treat it as rental_estimate_max.
Never place rent-related amounts under price or max_price.
Output JSON only. No explanations.

If the user mentions a specific street or address, "רחוב" extract it to the `address` field.
For example:
"apartment in Tel Aviv, Ben Yehuda street" → address = "Ben Yehuda street

say that the prices in shekels - ILS - new israeli shekel



"""

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an AI assistant that extracts real estate search filters from user questions in English or Hebrew.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.2,
                timeout=10
            )

            content = response["choices"][0]["message"]["content"]
            print("🧠 GPT Raw Output:\n", content)

            # Try extracting JSON from response
            match = re.search(r"\{.*\}", content, re.DOTALL)
            if match:
                criteria = json.loads(match.group(0))
                criteria["_raw"] = content.strip()  # Optional: keep full GPT reply
                return criteria
            else:
                print("❌ No JSON found in GPT output")
                return {"_raw": content.strip()}

        except Exception as e:
            print(f"❌ GPT Error: {e}")
            return {"_error": str(e)}


def build_response_message(criteria: dict, results: list, lang: str = "en") -> str:
    n = len(results)
    city = criteria.get("city")
    address = criteria.get("address")
    floor = criteria.get("floor")
    property_type = criteria.get("property_type")
    max_price = criteria.get("max_price")
    rent_max = criteria.get("rental_estimate_max")
    yield_min = criteria.get("yield_percent")
    min_rooms = criteria.get("min_rooms")
    max_rooms = criteria.get("max_rooms")
    min_floor = criteria.get("min_floor")
    max_floor = criteria.get("max_floor")

    if lang == "he":
        msg = f"נמצאו {n} נכסים"
        if city:
            msg += f" בעיר {city}"
        if address:
            msg += f", ברחוב {address}"
        if min_floor is not None and max_floor is not None and min_floor != max_floor:
            msg += f", בקומות {min_floor}–{max_floor}"
        elif max_floor:
            msg += f", עד קומה {max_floor}"
        elif min_floor:
            msg += f", מקומה {min_floor} ומעלה"
        if property_type:
            msg += f", מסוג {property_type}"
        if max_price:
            msg += f", במחיר רכישה של עד ₪{max_price:,}"
        if rent_max:
            msg += f", בשכירות משוערת של עד ₪{rent_max:,}"
        if yield_min:
            msg += f", עם תשואה משוערת של לפחות {yield_min:.1f}%"
        if min_rooms and max_rooms and min_rooms != max_rooms:
            msg += f", עם בין {min_rooms} ל־{max_rooms} חדרים"
        elif max_rooms:
            msg += f", עם עד {max_rooms} חדרים"
        elif min_rooms:
            msg += f", עם לפחות {min_rooms} חדרים"

        msg += "." if n > 0 else ". לא נמצאו נכסים מתאימים."

    else:
        msg = f"Found {n} properties"
        if city:
            msg += f" in {city}"
        if address:
            msg += f", on street {address}"
        if min_floor is not None and max_floor is not None and min_floor != max_floor:
            msg += f", on floors {min_floor}–{max_floor}"
        elif max_floor is not None:
            msg += f", up to floor {max_floor}"
        elif min_floor is not None:
            msg += f", from floor {min_floor} and up"
        if property_type:
            msg += f", type: {property_type}"
        if max_price:
            msg += f", with purchase price under ₪{max_price:,}"
        if rent_max:
            msg += f", with estimated rent under ₪{rent_max:,}"
        if yield_min:
            msg += f", with estimated yield of at least {yield_min:.1f}%"
        if min_rooms and max_rooms and min_rooms != max_rooms:
            msg += f", with {min_rooms}–{max_rooms} rooms"
        elif max_rooms:
            msg += f", with up to {max_rooms} rooms"
        elif min_rooms:
            msg += f", with at least {min_rooms} rooms"

        msg += "." if n > 0 else ". No matching properties found."

    return msg


def detect_language(text: str) -> str:
    return "he" if any("\u0590" <= c <= "\u05EA" for c in text) else "en"


def build_gpt_prompt(messages: list) -> list:
    """
    Convert list of Message ORM objects into OpenAI chat format.
    """
    prompt = [
        {
            "role": "system",
            "content": (
                "You are a helpful real estate assistant. "
                "Answer briefly and professionally. "
                "Ask follow-up questions if helpful. "
                "Use existing context from the chat if applicable."
            )
        }
    ]

    for msg in sorted(messages, key=lambda m: m.created_at):
        prompt.append({
            "role": msg.role,
            "content": msg.content
        })

    return prompt


def chat_with_gpt(messages: list) -> str:
    prompt = build_gpt_prompt(messages)

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=prompt,
            temperature=0.4
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        print("❌ GPT chat error:", e)
        return "Sorry, something went wrong with the assistant."



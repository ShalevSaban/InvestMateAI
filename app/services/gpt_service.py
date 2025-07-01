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
"apartment in Tel Aviv, Ben Yehuda street" → address = "Ben Yehuda street"

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

            match = re.search(r"\{.*\}", content, re.DOTALL)
            if match:
                criteria = json.loads(match.group(0))
                criteria["_raw"] = content.strip()
                return criteria
            else:
                return {"_raw": content.strip()}

        except Exception as e:
            print(f"❌ GPT Error: {e}")
            return {"_error": str(e)}

    @staticmethod
    def generate_gpt_insights(agent_id: str, text: str) -> dict:
        prompt = f"""
You are a business analyst specialized in real estate. Analyze the following client messages and return dashboard insights for a real estate agent.

Messages:
{text}

Output must be a valid JSON with the following format:
{{
  "summary": "...",
  "frequent_needs": ["...", "..."],
  "potential_opportunities": ["...", "..."],
  "recommended_actions": ["...", "..."]
}}

Output only the JSON. No explanations.
"""

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a dashboard assistant."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.4,
                timeout=15
            )

            content = response["choices"][0]["message"]["content"]
            print("📊 GPT Dashboard Output:\n", content)

            # Remove markdown block if it exists
            content = content.strip()
            if content.startswith("```json"):
                content = content.replace("```json", "").replace("```", "").strip()
            elif content.startswith("```"):
                content = content.replace("```", "").strip()

            # Extract JSON
            match = re.search(r"\{.*\}", content, re.DOTALL)
            if match:
                parsed = json.loads(match.group(0))
                if isinstance(parsed, dict):
                    return {
                        "summary": str(parsed.get("summary", "")),
                        "frequent_needs": [str(x) for x in parsed.get("frequent_needs", [])],
                        "potential_opportunities": [str(x) for x in parsed.get("potential_opportunities", [])],
                        "recommended_actions": [str(x) for x in parsed.get("recommended_actions", [])],
                    }

        except Exception as e:
            print("❌ GPT error:", e)
            return {
                "summary": "GPT error occurred",
                "frequent_needs": [],
                "potential_opportunities": [],
                "recommended_actions": [],
                "_error": str(e)
            }


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

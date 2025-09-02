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
- yield_percent (number or null)
- description_filters (array of relevant keywords found in the user's request related to description, like: "pool", "balcony", "city center", "near metro", etc.)


Output must be valid JSON only. Do not explain anything.
If the question is in Hebrew, translate internally and extract in English.

If the user mentions rent-related expressions (in English or Hebrew), such as:
- "rent", "rental price", "monthly rent", "for rent", "שכירות", "שכר דירה", "מחיר שכירות"
→ extract the amount as `rental_estimate_max`.

If the user uses words like:
- "buy", "purchase", "for sale", "לקנייה", "מחיר", "קנייה", "מכירה"
→ extract the amount as `price`, `min_price`, or `max_price`.

If the question clearly and explicitly includes both rent and purchase prices — return both `rental_estimate_max` and `max_price`.

However, if both rent-related and purchase-related words appear ambiguously (e.g. "purchase rent", "rent or buy" without clear prices), always prioritize **rent context**:
→ Set `rental_estimate_max`, and set price fields (like `price`, `min_price`, `max_price`) to null.

If the question contains the word "rent", assume the context is about renting — even if the word "buy" or "purchase" is also mentioned.

The presence of "rent" should default the context to rental — unless the user explicitly separates both options and gives two distinct prices.

Never duplicate values between rent and purchase fields unless both were explicitly mentioned by the user.


Output JSON only. No explanations.

If the user mentions a specific street or address, extract the **street name only** into the `address` field.

A "street" can be mentioned in various natural ways, in both English and Hebrew. Detect and extract the **street name without the word 'street' or 'רחוב'**.

Handle all of the following cases (case-insensitive):

#### 🏙️ English examples:
- "Ben Yehuda street" → address = "Ben Yehuda"
- "street Ben Yehuda" → address = "Ben Yehuda"
- "on Ben Yehuda st." or "on st. Ben Yehuda" → address = "Ben Yehuda"
- "in Tel Aviv, Ben Yehuda" → address = "Ben Yehuda"
- "apartment in Herzliya on Weizmann street" → address = "Weizmann"
- "flat at 12 Dizengoff" → address = "Dizengoff"
- "looking for a place in Arlozorov st" → address = "Arlozorov"

#### 🏠 Hebrew examples:
- "רחוב הרצל בתל אביב" → address = "הרצל"
- "מחפש דירה ברחוב אבן גבירול" → address = "אבן גבירול"
- "אזור גן העיר, דיזינגוף" → address = "דיזינגוף"
- "מחפש ברחוב יגאל אלון" → address = "יגאל אלון"

Do not include house numbers or city names in the `address` field.

Please follow these additional rules:

- If the user provides a street name in Hebrew (e.g., "רחוב דיזנגוף"), translate it into English (e.g., "Dizengoff Street") and place it in the `address` field. Do not include directional or contextual phrases (e.g., "במרכז העיר", "צפון") in the address.
  
say that the prices in shekels - ILS - new israeli shekel

If the user mentions general preferences or amenities (e.g., "with a pool", "near the metro", "city center", "north area", "south area", "near bus station", "balcony", "garden", "elevator", "parking", etc.), extract them as strings into a list under the key `description_filters`.

This includes location preferences and property features such as:

- "pool", "בריכה"
- "balcony", "מרפסת"
- "garden", "חצר"
- "elevator", "מעלית"
- "parking", "חניה"
- "near public transport", "near metro", "ליד תחנת רכבת", "קרוב לתחבורה ציבורית"
- "city center", "מרכז העיר", "במרכז"
- "north", "south", "east", "west", "צפון", "דרום", "מזרח", "מערב"

Translate Hebrew expressions into normalized English keywords. Examples:

- "צפון תל אביב" → "north area"
- "דרום תל אביב" → "south area"
- "במרכז העיר" or "Center" → "city center"

If the term is ambiguous (e.g., “Center”), assume the user means “city center” unless clearly stated otherwise.

Output all values in English. Do not explain or include translations in the output — only the normalized English terms in the `description_filters` list.

"""

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4-turbo",
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
                if "description_filters" not in criteria:
                    criteria["description_filters"] = []
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
                model="gpt-4-turbo",
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

    def estimate_property_metrics(self, price, city, address, rooms=None, floor=None, description=None):
        prompt = f"""
        A real estate property is listed for {price} ILS. It is located in the city of {city}, on {address}.
        {f"It has {rooms} rooms." if rooms else ""}
        {f"It is on the {floor} floor." if floor else ""}
        {f"Description: {description}" if description else ""}

        Based on this information, estimate:
        1. The expected monthly rental price (in ILS)
        2. The expected rental yield (in percentage)

        Respond only with a JSON object using the exact keys below.
        Do not include explanations or use alternative key names.

        Example format:
        {{
          "rental_estimate": 12345,
          "yield_percent": 3.5
        }}
        """

        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )

        content = response.choices[0].message.content.strip()

        # הסר עטיפת markdown אם קיימת (```json ... ```)
        if content.startswith("```json"):
            content = content.removeprefix("```json").removesuffix("```").strip()

        print("🔍 GPT response content:\n", content)

        try:
            parsed = json.loads(content)
            return parsed
        except Exception as e:
            print("❌ Failed to parse GPT content:", e)
            return {"rental_estimate": None, "yield_percent": None}


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
    description_filters = criteria.get("description_filters")

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
        if description_filters:
            msg += f", מסנני חיפוש: {', '.join(description_filters)}"
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
        if description_filters:
            msg += f", with features: {', '.join(description_filters)}"
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




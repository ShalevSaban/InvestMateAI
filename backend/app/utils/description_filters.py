# app/utils/description_filters.py

from typing import List
from app.models.property import Property
from sqlalchemy.sql import or_

FILTER_SYNONYMS = {
    "city center": ["city center", "center", "מרכז", "מרכז העיר"],
    "north area": ["north", "north area", "צפון", "צפון תל אביב"],
    "south area": ["south", "south area", "דרום", "דרום תל אביב"],
    "balcony": ["balcony", "מרפסת"],
    "pool": ["pool", "בריכה"],
    "elevator": ["elevator", "מעלית"],
    "parking": ["parking", "חניה"],
    "garden": ["garden", "חצר"],
    "near metro": ["near metro", "train", "תחבורה ציבורית", "רכבת"],
}


def build_description_filters(keywords: List[str]):
    conditions = []
    for keyword in keywords:
        synonyms = FILTER_SYNONYMS.get(keyword, [keyword])
        for syn in synonyms:
            # מחזיר תנאי SQLAlchemy אמיתי
            conditions.append(Property.description.ilike(f"%{syn}%"))
    return conditions

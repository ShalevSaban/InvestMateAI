# app/services/property_service.py
from decimal import Decimal
from functools import reduce
from operator import or_
from uuid import UUID

from sqlalchemy import func
from sqlalchemy.orm import Session
from app.models.property import Property
from app.models.agent import Agent
from app.schemas.property import PropertyCreate, PropertyUpdate
from fastapi import HTTPException, Depends
from app.database import get_db
from app.services.gpt_service import GPTService
from app.utils.description_filters import build_description_filters
from sqlalchemy.sql.elements import BinaryExpression


def create_property(db: Session, property_data: PropertyCreate, agent_id: UUID):
    data = property_data.dict()

    # אם לא סופק מחיר שכירות או תשואה – נבצע הערכה
    if not data.get("rental_estimate") or not data.get("yield_percent"):
        gpt = GPTService()
        estimated = gpt.estimate_property_metrics(
            price=data["price"],
            city=data["city"],
            address=data["address"],
            rooms=data.get("rooms"),
            floor=data.get("floor"),
            description=data.get("description"),
        )

        print("💬 Estimated values from GPT:", estimated)

        if data.get("rental_estimate") is None and estimated.get("rental_estimate") is not None:
            try:
                data["rental_estimate"] = Decimal(str(estimated["rental_estimate"]))
            except Exception as e:
                print("❌ rental_estimate conversion failed:", e)

        if data.get("yield_percent") is None and estimated.get("yield_percent") is not None:
            try:
                data["yield_percent"] = Decimal(str(estimated["yield_percent"]))
            except Exception as e:
                print("❌ yield_percent conversion failed:", e)
        print("📦 Final property data before save:", data)

    # יצירת המודל עם השדות
    new_property = Property(**data, agent_id=agent_id)
    db.add(new_property)
    db.commit()
    db.refresh(new_property)
    return new_property


def get_properties_for_agent(db: Session, agent: Agent):
    return db.query(Property).filter_by(agent_id=agent.id).all()


def get_property_by_id_for_agent(property_id: str, db: Session, agent: Agent):
    property = db.query(Property).filter_by(id=property_id, agent_id=agent.id).first()
    if not property:
        raise HTTPException(status_code=404, detail="Not found or unauthorized")
    return property


def update_property(property_id: str, updates: PropertyUpdate, db: Session, agent: Agent):
    property = db.query(Property).filter_by(id=property_id, agent_id=agent.id).first()
    if not property:
        raise HTTPException(status_code=404, detail="Not found or unauthorized")

    for field, value in updates.dict(exclude_unset=True).items():
        setattr(property, field, value)

    db.commit()
    db.refresh(property)
    return property


def delete_property(property_id: str, db: Session, agent: Agent):
    property = db.query(Property).filter_by(id=property_id, agent_id=agent.id).first()
    if not property:
        raise HTTPException(status_code=404, detail="Not found or unauthorized")

    db.delete(property)
    db.commit()


def search_properties_by_criteria(criteria: dict, db: Session = Depends(get_db)):
    query = db.query(Property)

    if criteria.get("agent_id"):
        query = query.filter(Property.agent_id == str(criteria["agent_id"]))
    if criteria.get("city"):
        query = query.filter(Property.city.ilike(f"%{criteria['city'].lower().strip()}%"))
    if criteria.get("address"):
        address = criteria["address"].strip().lower()
        query = query.filter(func.lower(Property.address).ilike(f"%{address}%"))
    if criteria.get("min_price"):
        query = query.filter(Property.price >= criteria["min_price"])
    if criteria.get("max_price"):
        query = query.filter(Property.price <= criteria["max_price"])
    if criteria.get("min_rooms") is not None:
        query = query.filter(Property.rooms >= criteria["min_rooms"])
    if criteria.get("max_rooms") is not None:
        query = query.filter(Property.rooms <= criteria["max_rooms"])
    if criteria.get("property_type"):
        query = query.filter(Property.property_type == criteria["property_type"].lower().strip())
    if criteria.get("min_floor") is not None:
        query = query.filter(Property.floor >= criteria["min_floor"])
    if criteria.get("max_floor") is not None:
        query = query.filter(Property.floor <= criteria["max_floor"])
    if criteria.get("rental_estimate_max") is not None:
        query = query.filter(Property.rental_estimate <= criteria["rental_estimate_max"])
    if criteria.get("yield_percent") is not None:
        query = query.filter(Property.yield_percent >= criteria["yield_percent"])

    # 💡 חדש: תיאור חכם עם נרדפות
    desc_conditions = build_description_filters(criteria["description_filters"])
    desc_conditions = [cond for cond in desc_conditions if isinstance(cond, BinaryExpression)]

    print("✅ Safe description conditions:", desc_conditions)

    if desc_conditions:
        or_expression = reduce(lambda a, b: or_(a, b), desc_conditions)
        query = query.filter(or_expression)
    return query.all()


def delete_all_properties_for_agent(db: Session, agent_id: UUID) -> int:
    deleted_count = (
        db.query(Property)
            .filter(Property.agent_id == agent_id)
            .delete(synchronize_session=False)
    )
    db.commit()
    return deleted_count

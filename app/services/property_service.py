# app/services/property_service.py

from sqlalchemy.orm import Session
from app.models.property import Property
from app.models.agent import Agent
from app.schemas.property import PropertyCreate, PropertyUpdate
from fastapi import HTTPException, Depends
from app.database import get_db


def create_property(data: PropertyCreate, db: Session, agent: Agent) -> Property:
    new_property = Property(
        city=data.city.lower().strip(),
        address=data.address.lower().strip(),
        price=data.price,
        agent_id=agent.id
    )

    optional_fields = [
        "yield_percent", "property_type", "rooms",
        "floor", "description", "rental_estimate"
    ]

    for field in optional_fields:
        value = getattr(data, field, None)
        if value is not None:
            setattr(new_property, field, value)

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
        query = query.filter(Property.address.ilike(f"%{criteria['address']}%"))
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

    return query.all()

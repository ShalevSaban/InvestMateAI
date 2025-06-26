# app/services/property_service.py

from sqlalchemy.orm import Session
from app.models.property import Property
from app.models.agent import Agent
from app.schemas.property import PropertyCreate, PropertyUpdate
from fastapi import HTTPException


def create_property(data: PropertyCreate, db: Session, agent: Agent) -> Property:
    new_property = Property(
        city=data.city,
        address=data.address,
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

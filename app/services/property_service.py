from sqlalchemy.orm import Session
from app.models.property import Property
from app.schemas.property import PropertyCreate, PropertyUpdate
from fastapi import HTTPException


def create_property(data: PropertyCreate, db: Session):
    prop = Property(**data.model_dump())
    db.add(prop)
    db.commit()
    db.refresh(prop)
    return prop


def get_all_properties(db: Session):
    return db.query(Property).all()


def get_property(property_id: str, db: Session):
    prop = db.query(Property).get(property_id)
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")
    return prop


def update_property(property_id: str, updates: PropertyUpdate, db: Session):
    prop = get_property(property_id, db)
    for field, value in updates.model_dump(exclude_unset=True).items():
        setattr(prop, field, value)
    db.commit()
    db.refresh(prop)
    return prop


def delete_property(property_id: str, db: Session):
    prop = get_property(property_id, db)
    db.delete(prop)
    db.commit()

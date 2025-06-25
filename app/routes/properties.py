from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.property import PropertyCreate, PropertyOut, PropertyUpdate
from app.services.property_service import (
    create_property, get_all_properties, get_property,
    update_property, delete_property
)
from app.database import SessionLocal

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=PropertyOut, status_code=201)
def create_property_route(data: PropertyCreate, db: Session = Depends(get_db)):
    return create_property(data, db)


@router.get("/", response_model=list[PropertyOut])
def get_properties_route(db: Session = Depends(get_db)):
    return get_all_properties(db)


@router.get("/{property_id}", response_model=PropertyOut)
def get_property_route(property_id: str, db: Session = Depends(get_db)):
    return get_property(property_id, db)


@router.put("/{property_id}", response_model=PropertyOut)
def update_property_route(property_id: str, updates: PropertyUpdate, db: Session = Depends(get_db)):
    return update_property(property_id, updates, db)


@router.delete("/{property_id}", status_code=204)
def delete_property_route(property_id: str, db: Session = Depends(get_db)):
    delete_property(property_id, db)
    return

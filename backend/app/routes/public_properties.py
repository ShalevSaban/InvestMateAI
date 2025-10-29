from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.property import Property
from app.schemas.property import PublicPropertyOut

router = APIRouter(prefix="/public", tags=["Public"])


@router.get("/properties", response_model=list[PublicPropertyOut])
def get_public_properties(db: Session = Depends(get_db)):
    return db.query(Property).all()


@router.get("/properties/{property_id}", response_model=PublicPropertyOut)
def get_public_property(property_id: str, db: Session = Depends(get_db)):
    property_obj = db.query(Property).filter_by(id=property_id).first()
    if not property_obj:
        raise HTTPException(status_code=404, detail="Property not found")
    return property_obj

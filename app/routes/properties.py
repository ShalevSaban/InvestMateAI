# app/routes/properties.py

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.property import PropertyCreate, PropertyOut, PropertyUpdate
from app.services.property_service import (
    create_property,
    get_properties_for_agent,
    get_property_by_id_for_agent,
    update_property,
    delete_property,
    delete_all_properties_for_agent
)
from app.utils.auth_deps import get_current_agent
from app.models.agent import Agent
from app.utils.aws_s3 import generate_presigned_view_url, upload_file_to_s3
from app.models.property import Property
import os

router = APIRouter()


@router.post("/", response_model=PropertyOut, status_code=201)
def create_property_route(
        data: PropertyCreate,
        db: Session = Depends(get_db),
        current_agent: Agent = Depends(get_current_agent)
):
    return create_property(db, data, current_agent.id)


@router.get("/", response_model=list[PropertyOut])
def get_properties_route(
        db: Session = Depends(get_db),
        current_agent: Agent = Depends(get_current_agent)
):
    return get_properties_for_agent(db, current_agent)


@router.get("/{property_id}", response_model=PropertyOut)
def get_property_route(
        property_id: str,
        db: Session = Depends(get_db),
        current_agent: Agent = Depends(get_current_agent)
):
    return get_property_by_id_for_agent(property_id, db, current_agent)


@router.put("/{property_id}", response_model=PropertyOut)
def update_property_route(
        property_id: str,
        updates: PropertyUpdate,
        db: Session = Depends(get_db),
        current_agent: Agent = Depends(get_current_agent)
):
    return update_property(property_id, updates, db, current_agent)


@router.delete("/{property_id}", status_code=204)
def delete_property_route(
        property_id: str,
        db: Session = Depends(get_db),
        current_agent: Agent = Depends(get_current_agent)
):
    delete_property(property_id, db, current_agent)
    return


@router.post("/{property_id}/upload-image")
async def upload_property_image(
        property_id: str,
        file: UploadFile = File(...),
        db: Session = Depends(get_db),
        current_agent: Agent = Depends(get_current_agent)
):
    property_obj = db.query(Property).filter_by(id=property_id, agent_id=current_agent.id).first()
    if not property_obj:
        raise HTTPException(status_code=404, detail="Property not found or unauthorized")

    # דינמית לפי סיומת הקובץ
    extension = os.path.splitext(file.filename)[-1] or ".jpg"
    key = f"property_images/{property_id}{extension}"

    content = await file.read()
    content_type = file.content_type or "image/jpeg"

    success = upload_file_to_s3(key, content, content_type)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to upload image")

    property_obj.image_url = key
    db.commit()
    db.refresh(property_obj)

    return {"message": "Image uploaded successfully", "file_key": key}


@router.get("/{property_id}/image-url")
def get_property_image_url(
        property_id: str,
        db: Session = Depends(get_db)
):
    property_obj = db.query(Property).filter_by(id=property_id).first()

    print(f"🔍 Property: {property_id}")
    print(f"🔍 image_url: {property_obj.image_url if property_obj else 'NOT FOUND'}")

    if not property_obj or not property_obj.image_url:
        raise HTTPException(status_code=404, detail="Image not found")

    url = generate_presigned_view_url(property_obj.image_url)
    if not url:
        raise HTTPException(status_code=500, detail="Failed to generate image URL")

    return {"image_url": url}


@router.delete("/", response_model=dict)
def delete_all_properties_route(
        db: Session = Depends(get_db),
        current_agent: Agent = Depends(get_current_agent)
):
    deleted_count = delete_all_properties_for_agent(db, current_agent.id)
    return {"message": f"{deleted_count} properties deleted successfully."}

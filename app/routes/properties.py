from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app.schemas.property import PropertyCreate, PropertyOut, PropertyUpdate
from app.services.property_service import (
    create_property, get_all_properties, get_property,
    update_property, delete_property
)
from app.database import SessionLocal
from app.utils.aws_s3 import s3_client, generate_presigned_view_url
import os
from app.models.property import Property

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


@router.post("/properties/{property_id}/upload-image")
async def upload_property_image(property_id: str, file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        # שם הקובץ ב-S3
        key = f"property_images/{property_id}.jpg"
        content = await file.read()
        bucket = os.getenv("AWS_S3_BUCKET_NAME")

        # העלאה ל-S3
        s3_client.put_object(
            Bucket=bucket,
            Key=key,
            Body=content,
            ContentType=file.content_type
        )

        # עדכון במסד: שומר רק את ה-key (לא URL!)
        property_obj = db.query(Property).filter(Property.id == property_id).first()
        if not property_obj:
            raise HTTPException(status_code=404, detail="Property not found")

        property_obj.image_url = key  # ✅ רק key, בלי https
        db.commit()
        db.refresh(property_obj)

        return {"message": "Image uploaded successfully", "file_key": key}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


@router.get("/properties/{property_id}/image-url")  ##לתקן או להפוך לציבורי
def get_property_image_url(property_id: str, db: Session = Depends(get_db)):
    property_obj = db.query(Property).filter(Property.id == property_id).first()
    if not property_obj or not property_obj.image_url:
        raise HTTPException(status_code=404, detail="Image not found")

    url = generate_presigned_view_url(property_obj.image_url)
    if not url:
        raise HTTPException(status_code=500, detail="Failed to generate signed URL")
    print("DEBUG presigned URL:", url)
    return {"image_url": url}

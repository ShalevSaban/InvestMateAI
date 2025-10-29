# app/utils/aws_s3.py

import boto3
import os
from botocore.exceptions import ClientError

# טוען משתני סביבה
AWS_REGION = os.getenv("AWS_S3_REGION", "us-east-2")
AWS_BUCKET = os.getenv("AWS_S3_BUCKET_NAME")
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

# יצירת לקוח S3
s3_client = boto3.client(
    "s3",
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY
)


def upload_file_to_s3(key: str, content: bytes, content_type: str = "image/jpeg") -> bool:
    """Upload binary content to S3."""

    try:
        s3_client.put_object(
            Bucket=AWS_BUCKET,
            Key=key,
            Body=content,
            ContentType=content_type
        )
        return True
    except ClientError as e:
        print(f"[S3] Upload failed: {e}")
        return False


def generate_presigned_view_url(key: str, expires_in: int = 3600) -> str | None:
    """Generate a presigned GET URL for a given S3 object key."""
    print("🧾 AWS_ACCESS_KEY_ID:", os.getenv("AWS_ACCESS_KEY_ID"))
    print("🧾 AWS_REGION:", os.getenv("AWS_REGION"))

    try:
        return s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": AWS_BUCKET, "Key": key},
            ExpiresIn=expires_in
        )
    except ClientError as e:
        print(f"[S3] Presigned URL generation failed: {e}")
        return None


def delete_s3_object(key: str) -> bool:
    """Delete an object from S3."""
    try:
        s3_client.delete_object(Bucket=AWS_BUCKET, Key=key)
        return True
    except ClientError as e:
        print(f"[S3] Delete failed: {e}")
        return False

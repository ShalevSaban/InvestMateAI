import boto3
from botocore.exceptions import ClientError
import os
from dotenv import load_dotenv

load_dotenv()

s3_client = boto3.client(
    "s3",
    region_name=os.getenv("AWS_S3_REGION"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
)


def generate_presigned_view_url(filename: str, expires_in: int = 3600):
    try:
        url = s3_client.generate_presigned_url(
            "get_object",
            Params={
                "Bucket": os.getenv("AWS_S3_BUCKET_NAME"),
                "Key": filename
            },
            ExpiresIn=expires_in
        )

        return url
    except ClientError as e:
        print(f"Failed to generate presigned GET URL: {e}")
        return None

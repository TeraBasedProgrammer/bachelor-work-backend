import boto3
from fastapi import HTTPException

from app.config.settings.base import settings

s3 = boto3.client(
    service_name="s3",
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_KEY,
    region_name=settings.AWS_REGION,
)
import mimetypes
from typing import BinaryIO, Optional


def upload_file_to_s3(
    file: BinaryIO, filename: str, content_type: Optional[str] = None
) -> str:
    """
    Upload a file to S3 bucket.

    Args:
        file: File-like object containing the file data
        filename: Name of the file to be stored in S3
        content_type: Optional MIME type of the file. If not provided, will be guessed from filename.

    Returns:
        str: URL of the uploaded file in S3
    """
    if not content_type:
        content_type = mimetypes.guess_type(filename)[0]

    if not content_type:
        content_type = "application/octet-stream"

    allowed_types = [
        "image/",
        "video/",
        "application/pdf",
    ]

    if not any(content_type.startswith(t) for t in allowed_types):
        raise ValueError(
            f"Invalid file type. Must be an image, video or PDF. Got: {content_type}"
        )

    try:
        s3.upload_fileobj(
            file,
            settings.AWS_BUCKET_NAME,
            filename,
            ExtraArgs={"ContentType": content_type},
        )

        url = f"{settings.AWS_S3_ENDPOINT}/{filename}"
        return url

    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Error uploading file to S3: {str(e)}"
        )

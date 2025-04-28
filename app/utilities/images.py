import io
import uuid
from typing import Optional

import httpx
from fastapi import UploadFile


async def download_image(url: str, filename: Optional[str] = None) -> UploadFile:
    """
    Downloads an image from a URL and converts it to FastAPI's UploadFile format.

    Args:
        url: The URL of the image to download
        filename: Optional filename to use. If not provided, generates a UUID

    Returns:
        UploadFile object containing the downloaded image
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()

        content = response.content
        content_type = response.headers.get("content-type", "application/octet-stream")

        if not filename:
            extension = content_type.split("/")[-1]
            filename = f"{uuid.uuid4()}.{extension}"

        file = io.BytesIO(content)

        return UploadFile(file=file, filename=filename, size=len(content))

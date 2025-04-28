from typing import Optional
from uuid import UUID

from fastapi import HTTPException, UploadFile, status
from pydantic import BaseModel

from app.repository.base import BaseRepository
from app.utilities.s3 import upload_file_to_s3_async


class BaseService:
    async def _validate_instance_exists(
        self, repository: BaseRepository, instance_id: int
    ) -> None:
        if not await repository.exists_by_id(instance_id):
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                detail=f"{repository.model.__name__} is not found",
            )

    async def _upload_files_to_s3(
        self,
        data: BaseModel,
        upload_tasks: tuple[str, ...],
    ) -> None:
        user_id: UUID = getattr(data, "user_id", None) or getattr(data, "id", None)

        for field_name, filename in upload_tasks:
            file_obj: Optional[UploadFile | str] = getattr(data, field_name, None)
            if file_obj:
                uploaded_url = await upload_file_to_s3_async(
                    file_obj,
                    f"{user_id}/{filename}",
                    file_obj.content_type,
                )
                setattr(data, field_name, uploaded_url)

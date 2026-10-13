from uuid import UUID

from fastapi import APIRouter
from pydantic import BaseModel, Field

from .config import settings

# Allow-list: mime type -> (kind, extension). Anything not listed is rejected.
ALLOWED_TYPES = {
    "application/pdf": ("doc", "pdf"),
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": ("doc", "docx"),
    "text/plain": ("doc", "txt"),
    "audio/webm": ("audio", "webm"),
    "audio/mpeg": ("audio", "mp3"),
    "audio/mp4": ("audio", "m4a"),
    "audio/wav": ("audio", "wav"),
}


class CreateFileRequest(BaseModel):
    mime_type: str
    size_bytes: int = Field(gt=0, le=settings.max_upload_size)


class CreateFileResponse(BaseModel):
    file_id: UUID
    upload_url: str
    upload_headers: dict[str, str]


router = APIRouter()

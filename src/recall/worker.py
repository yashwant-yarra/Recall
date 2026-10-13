import asyncio
import logging
from contextlib import asynccontextmanager
from uuid import UUID

import google.auth
from fastapi import FastAPI, Request
from google.cloud import storage
from sqlalchemy import text

from .config import settings
from .db import make_engine
from .extract import extract_text

# uvicorn only configures its own loggers; without this, INFO from this module is dropped.
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.engine = make_engine()
    credentials, project = google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
    app.state.bucket = storage.Client(credentials=credentials, project=project).bucket(settings.gcs_bucket)
    yield
    await app.state.engine.dispose()


app = FastAPI(lifespan=lifespan)


@app.post("/")
async def handle_event(request: Request):
    event = await request.json()
    name = event.get("name", "")
    file_id = file_id_from_object_name(name)
    if file_id is None:
        logger.info("Ignoring object %s", name)
        return {"status": "ignored"}

    engine = request.app.state.engine
    # Atomic claim: only one delivery of a (possibly duplicated) event gets the row.
    async with engine.begin() as conn:
        result = await conn.execute(
            text(
                "UPDATE files SET status = 'processing' "
                "WHERE id = :id AND status = 'pending' "
                "RETURNING gcs_path, mime_type"
            ),
            {"id": file_id},
        )
        row = result.first()
    if row is None:
        logger.info("Skipping %s: not pending", file_id)
        return {"status": "skipped"}

    # Any failure must land in 'failed', or the row stays stuck in 'processing'.
    try:
        data = await asyncio.to_thread(request.app.state.bucket.blob(row.gcs_path).download_as_bytes)
        pages = await asyncio.to_thread(extract_text, data, row.mime_type)
        if not any(page.strip() for page in pages):
            raise ValueError("No extractable text")
        logger.info("Extracted %s: %d pages, %d chars", file_id, len(pages), sum(len(p) for p in pages))
        status, error = "ready", None
    except Exception as e:
        logger.exception("Processing failed for %s", file_id)
        status, error = "failed", str(e)

    async with engine.begin() as conn:
        await conn.execute(
            text("UPDATE files SET status = :status, error = :error WHERE id = :id"),
            {"status": status, "error": error, "id": file_id},
        )
    return {"status": status}


def file_id_from_object_name(name: str) -> UUID | None:
    parts = name.split("/")
    if len(parts) != 4 or parts[0] != "users" or parts[2] != "docs":
        return None
    stem = parts[3].rsplit(".", 1)[0]
    try:
        return UUID(stem)
    except ValueError:
        return None

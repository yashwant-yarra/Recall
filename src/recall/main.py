import logging
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, Request
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import create_async_engine
import google.auth
from google.cloud import storage

from . import auth

from .config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    connect_args = {"prepare_threshold": None}
    engine = create_async_engine(settings.database_url, echo=settings.db_echo, pool_pre_ping=True, connect_args=connect_args)
    app.state.engine = engine
    credentials, project = google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
    app.state.gcs_credentials = credentials
    app.state.gcs_bucket = storage.Client(credentials=credentials, project=project).bucket(settings.gcs_bucket)
    yield
    await engine.dispose()

app = FastAPI(lifespan=lifespan)

logger = logging.getLogger(__name__)

@app.get("/health")
def read_health():
    return {"status": "ok"}

@app.get("/health/db")
async def read_health_db(request: Request):
    try:
        async with request.app.state.engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        return {"status": "ok"}
    except OperationalError as e:
        logger.exception("Database health check failed")
        raise HTTPException(status_code=503, detail="Database connection failed") from e
@app.get("/me")
def read_current_user(user_id: str = Depends(auth.get_current_user_id)):
    """
    Endpoint to get the current user ID.
    Raises an HTTPException if the user ID is not set in the environment.
    """
    return {"user_id": user_id}
import logging
from fastapi import FastAPI, Request, HTTPException
from .config import settings
from sqlalchemy.ext.asyncio import create_async_engine
from contextlib import asynccontextmanager
from sqlalchemy import text
from sqlalchemy.exc import OperationalError

@asynccontextmanager
async def lifespan(app: FastAPI):
    connect_args = {"prepare_threshold": None}
    engine = create_async_engine(settings.database_url, echo=settings.db_echo, pool_pre_ping=True, connect_args=connect_args)
    app.state.engine = engine
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
    
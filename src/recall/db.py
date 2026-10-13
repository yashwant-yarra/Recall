from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from .config import settings

def make_engine() -> AsyncEngine:
    # prepare_threshold=None: Neon's pooler (PgBouncer, transaction mode) breaks server-side prepared statements.
    connect_args = {"prepare_threshold": None}
    return create_async_engine(settings.database_url, echo=settings.db_echo, pool_pre_ping=True, connect_args=connect_args)
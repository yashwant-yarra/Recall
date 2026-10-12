"""create users and files

Revision ID: 785c087a8f49
Revises: 
Create Date: 2026-10-12 11:46:42.825189

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '785c087a8f49'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""
        CREATE TABLE users (
            id TEXT PRIMARY KEY,
            email TEXT NOT NULL UNIQUE,
            created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
        )
    """)
    op.execute("""
        CREATE TABLE files (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            user_id TEXT NOT NULL REFERENCES users(id),
            kind TEXT NOT NULL CHECK (kind IN ('audio','doc')),
            gcs_path TEXT NOT NULL UNIQUE,
            mime_type TEXT NOT NULL,
            size_bytes BIGINT NOT NULL CHECK (size_bytes >= 0),
            status TEXT NOT NULL DEFAULT 'uploaded' CHECK (status IN ('uploaded','processing','ready','failed')),
            error TEXT,
            created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
        )
    """)
    op.execute("""
        CREATE INDEX files_user_id_created_at_idx ON files (user_id, created_at DESC)
    """)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP TABLE files")
    op.execute("DROP TABLE users")

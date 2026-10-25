"""files claimed_at and attempts

Revision ID: a39bcbe0c67c
Revises: 353476a31d58
Create Date: 2026-10-25 11:22:01.975064

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a39bcbe0c67c'
down_revision: Union[str, Sequence[str], None] = '353476a31d58'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # claimed_at: when the current processing claim started, so an abandoned claim can expire.
    # attempts: claims taken so far, so a file that keeps crashing the worker eventually fails.
    op.execute("""
        ALTER TABLE files
            ADD COLUMN claimed_at TIMESTAMPTZ,
            ADD COLUMN attempts INTEGER NOT NULL DEFAULT 0
    """)
    # Rows already 'processing' get a claim time, so the lease can expire them
    # (NULL never compares as older than the lease).
    op.execute("""
        UPDATE files SET claimed_at = now(), attempts = 1 WHERE status = 'processing'
    """)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("""
        ALTER TABLE files
            DROP COLUMN attempts,
            DROP COLUMN claimed_at
    """)

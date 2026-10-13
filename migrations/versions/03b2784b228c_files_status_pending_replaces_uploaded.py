"""files status pending replaces uploaded

Revision ID: 03b2784b228c
Revises: 785c087a8f49
Create Date: 2026-10-13 10:42:36.544827

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '03b2784b228c'
down_revision: Union[str, Sequence[str], None] = '785c087a8f49'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""
        ALTER TABLE files DROP CONSTRAINT files_status_check
    """)
    op.execute("""
        ALTER TABLE files ADD CONSTRAINT files_status_check CHECK (status IN ('pending', 'processing', 'ready', 'failed'))
    """)
    op.execute("""
        ALTER TABLE files ALTER COLUMN status SET DEFAULT 'pending'
    """)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("""
        ALTER TABLE files ALTER COLUMN status SET DEFAULT 'uploaded'
    """)
    op.execute("""
        ALTER TABLE files DROP CONSTRAINT files_status_check
    """)
    op.execute("""
        ALTER TABLE files ADD CONSTRAINT files_status_check CHECK (status IN ('uploaded', 'processing', 'ready', 'failed'))
    """)
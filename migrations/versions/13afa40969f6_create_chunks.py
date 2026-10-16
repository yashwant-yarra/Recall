"""create chunks

Revision ID: 13afa40969f6
Revises: 03b2784b228c
Create Date: 2026-10-13 17:02:27.857311

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '13afa40969f6'
down_revision: Union[str, Sequence[str], None] = '03b2784b228c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""
        CREATE TABLE chunks (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            file_id UUID NOT NULL REFERENCES files(id) ON DELETE CASCADE,
            user_id TEXT NOT NULL,
            chunk_no INT NOT NULL,
            page INT,
            content TEXT NOT NULL,
            embedding halfvec(768) NOT NULL,
            tsv tsvector GENERATED ALWAYS AS (to_tsvector('english', content)) STORED,
            created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
            UNIQUE (file_id, chunk_no)
            )
    """)
    op.execute("""
        CREATE INDEX chunks_embedding_idx ON chunks USING hnsw (embedding halfvec_cosine_ops)
    """)
    op.execute("""
        CREATE INDEX chunks_tsv_idx ON chunks USING gin (tsv)
    """)
    op.execute("""
        CREATE INDEX chunks_user_id_idx ON chunks (user_id)
    """)

def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP TABLE chunks")

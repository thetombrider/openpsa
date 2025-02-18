"""add_cancelled_to_resource_allocation_status

Revision ID: 35fb47a6aad3
Revises: a795603ab7ef
Create Date: 2025-02-18 00:46:41.396303

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '35fb47a6aad3'
down_revision: Union[str, None] = 'a795603ab7ef'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # PostgreSQL
    op.execute("ALTER TYPE resourceallocationstatus ADD VALUE IF NOT EXISTS 'CANCELLED'")

def downgrade() -> None:
    # Non è possibile rimuovere valori da un enum in PostgreSQL
    pass

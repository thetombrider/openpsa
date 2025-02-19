"""rename_role_columns

Revision ID: 5220168451a2
Revises: 9ae100df771a
Create Date: 2025-02-19 23:52:56.632486

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5220168451a2'
down_revision: Union[str, None] = '9ae100df771a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass

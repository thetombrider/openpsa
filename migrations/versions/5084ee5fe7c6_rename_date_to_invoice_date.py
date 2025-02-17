"""rename_date_to_invoice_date

Revision ID: 5084ee5fe7c6
Revises: 5c5fbf2e81d6
Create Date: 2025-02-17 11:16:21.948115

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5084ee5fe7c6'
down_revision: Union[str, None] = '5c5fbf2e81d6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('invoices', 'date', new_column_name='invoice_date')

def downgrade() -> None:
    op.alter_column('invoices', 'invoice_date', new_column_name='date')
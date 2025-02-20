"""add_billing_rate_history_to_line_items

Revision ID: e003aecc5859
Revises: 5d7c21fdd8ff
Create Date: 2025-02-20 15:11:35.491341

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e003aecc5859'
down_revision: Union[str, None] = '5d7c21fdd8ff'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Aggiungi le colonne a invoice_line_items
    op.add_column('invoice_line_items', 
        sa.Column('billing_rate_id', sa.Integer(), nullable=True))
    op.add_column('invoice_line_items', 
        sa.Column('rate_at_creation', sa.Numeric(10, 2)))
    op.add_column('invoice_line_items', 
        sa.Column('currency_at_creation', sa.String()))
    
    # Crea la foreign key
    op.create_foreign_key(
        'fk_invoice_line_items_billing_rate',
        'invoice_line_items', 'billing_rates',
        ['billing_rate_id'], ['id']
    )

def downgrade() -> None:
    # Rimuovi la foreign key
    op.drop_constraint(
        'fk_invoice_line_items_billing_rate',
        'invoice_line_items',
        type_='foreignkey'
    )
    
    # Rimuovi le colonne nell'ordine corretto
    op.drop_column('invoice_line_items', 'currency_at_creation')
    op.drop_column('invoice_line_items', 'rate_at_creation')
    op.drop_column('invoice_line_items', 'billing_rate_id')

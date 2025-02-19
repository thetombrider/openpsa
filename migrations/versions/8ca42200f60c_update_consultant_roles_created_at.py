"""update_consultant_roles_created_at

Revision ID: 8ca42200f60c
Revises: 4a963529e876
Create Date: 2025-02-20 00:12:31.578316

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy.sql import text

# revision identifiers, used by Alembic.
revision: str = '8ca42200f60c'
down_revision: Union[str, None] = '4a963529e876'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Aggiorna i valori NULL in consultant_roles
    op.execute("""
        UPDATE consultant_roles 
        SET created_at = CURRENT_TIMESTAMP 
        WHERE created_at IS NULL
    """)
    
    # Modifica consultant_roles
    op.alter_column('consultant_roles', 'created_at',
               existing_type=sa.DateTime(),
               server_default=sa.text('CURRENT_TIMESTAMP'),
               nullable=False)
    
    # Verifica e rimuovi gli indici se esistono
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    indices = inspector.get_indexes('project_billing_rates')
    existing_indices = [idx['name'] for idx in indices]
    
    if 'ix_project_billing_rates_billing_rate_id' in existing_indices:
        op.drop_index('ix_project_billing_rates_billing_rate_id', 
                     table_name='project_billing_rates')
    if 'ix_project_billing_rates_project_id' in existing_indices:
        op.drop_index('ix_project_billing_rates_project_id', 
                     table_name='project_billing_rates')
    
    # Modifica solo le colonne non-PK
    op.alter_column('project_billing_rates', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True,
               existing_server_default=sa.text('CURRENT_TIMESTAMP'))
    op.alter_column('project_billing_rates', 'active',
               existing_type=sa.BOOLEAN(),
               nullable=True,
               existing_server_default=sa.text('true'))

    # Verifica esistenza colonna prima di rimuoverla
    inspector = sa.inspect(conn)
    columns = [c['name'] for c in inspector.get_columns('resource_allocations')]
    if 'allocation_percentage' in columns:
        op.drop_column('resource_allocations', 'allocation_percentage')


def downgrade() -> None:
    # Prima gestisci resource_allocations
    op.add_column('resource_allocations',
        sa.Column('allocation_percentage', 
                 sa.DOUBLE_PRECISION(precision=53),
                 nullable=True)
    )
    
    op.execute("""
        UPDATE resource_allocations 
        SET allocation_percentage = 100.0 
        WHERE allocation_percentage IS NULL
    """)
    
    op.alter_column('resource_allocations', 'allocation_percentage',
                   existing_type=sa.DOUBLE_PRECISION(precision=53),
                   nullable=False)

    # Ripristina le colonne non-PK
    op.alter_column('project_billing_rates', 'active',
               existing_type=sa.BOOLEAN(),
               nullable=False,
               existing_server_default=sa.text('true'))
    op.alter_column('project_billing_rates', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False,
               existing_server_default=sa.text('CURRENT_TIMESTAMP'))
               
    # Ricrea gli indici
    op.create_index('ix_project_billing_rates_project_id',
                   'project_billing_rates', ['project_id'])
    op.create_index('ix_project_billing_rates_billing_rate_id',
                   'project_billing_rates', ['billing_rate_id'])
    
    # Ripristina consultant_roles
    op.alter_column('consultant_roles', 'created_at',
               existing_type=sa.DateTime(),
               server_default=None,
               nullable=True)

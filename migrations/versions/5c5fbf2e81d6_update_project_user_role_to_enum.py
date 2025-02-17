"""update_project_user_role_to_enum

Revision ID: 5c5fbf2e81d6
Revises: 021c9bd12bc7
Create Date: 2025-02-17 10:22:36.007972

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5c5fbf2e81d6'
down_revision: Union[str, None] = '021c9bd12bc7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Crea il nuovo enum se non esiste
    op.execute("DROP TYPE IF EXISTS consultantrole CASCADE")
    consultantrole = sa.Enum(
        'JUNIOR', 'MID', 'SENIOR', 'MASTER', 'PRINCIPAL',
        name='consultantrole'
    )
    consultantrole.create(op.get_bind(), checkfirst=False)

    # Aggiorna la colonna role in project_users
    op.drop_column('project_users', 'role')
    op.add_column('project_users',
        sa.Column('role', sa.Enum('JUNIOR', 'MID', 'SENIOR', 'MASTER', 'PRINCIPAL',
                                name='consultantrole'), nullable=True)
    )

    # Aggiorna la colonna role in resource_allocations
    op.drop_column('resource_allocations', 'role')
    op.add_column('resource_allocations',
        sa.Column('role', sa.Enum('JUNIOR', 'MID', 'SENIOR', 'MASTER', 'PRINCIPAL',
                                name='consultantrole'), nullable=True)
    )


def downgrade() -> None:
    # Converti le colonne role back to string
    op.drop_column('project_users', 'role')
    op.add_column('project_users',
        sa.Column('role', sa.String(), nullable=True)
    )
    
    op.drop_column('resource_allocations', 'role')
    op.add_column('resource_allocations',
        sa.Column('role', sa.String(), nullable=True)
    )

    # Drop the enum
    op.execute("DROP TYPE IF EXISTS consultantrole")

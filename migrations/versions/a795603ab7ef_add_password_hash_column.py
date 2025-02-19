"""add_password_hash_column

Revision ID: a795603ab7ef
Revises: 5084ee5fe7c6
Create Date: 2025-02-17 19:33:29.637362

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a795603ab7ef'
down_revision: Union[str, None] = '5084ee5fe7c6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # 1. Aggiungi la colonna permettendo NULL inizialmente
    op.add_column('users', sa.Column('password_hash', sa.String(length=255), nullable=True))
    
    # 2. Imposta un valore di default per i record esistenti
    op.execute("UPDATE users SET password_hash = 'changeme'")
    
    # 3. Poi rendi la colonna NOT NULL
    op.alter_column('users', 'password_hash',
               existing_type=sa.String(length=255),
               nullable=False)

def downgrade() -> None:
    op.drop_column('users', 'password_hash')
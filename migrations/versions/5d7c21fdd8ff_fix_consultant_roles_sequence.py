"""fix_consultant_roles_sequence

Revision ID: 5d7c21fdd8ff
Revises: 8ca42200f60c
Create Date: 2025-02-20
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '5d7c21fdd8ff'
down_revision: Union[str, None] = '8ca42200f60c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # Resetta la sequenza al massimo ID esistente
    op.execute("""
        SELECT setval('consultant_roles_id_seq', 
                     (SELECT COALESCE(MAX(id), 0) FROM consultant_roles), 
                     true)
    """)

def downgrade() -> None:
    # Non è necessario fare nulla nel downgrade poiché 
    # la sequenza si adatterà automaticamente
    pass

"""add owner to projects

Revision ID: 0002_owner
Revises: 0001_init
Create Date: 2025-08-11 00:00:00
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0002_owner'
down_revision = '0001_init'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('projects', sa.Column('owner', sa.String(length=320), nullable=True))
    op.execute("""UPDATE projects SET owner = 'unknown@local' WHERE owner IS NULL""")
    op.alter_column('projects', 'owner', nullable=False)

def downgrade():
    op.drop_column('projects', 'owner')

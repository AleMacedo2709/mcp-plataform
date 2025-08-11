"""add tasks table

Revision ID: 0003_tasks
Revises: 0002_owner
Create Date: 2025-08-11 00:00:00
"""
from alembic import op
import sqlalchemy as sa

revision = '0003_tasks'
down_revision = '0002_owner'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('tasks',
        sa.Column('id', sa.String(length=64), nullable=False),
        sa.Column('type', sa.String(length=100), nullable=False),
        sa.Column('filename', sa.String(length=500), nullable=True),
        sa.Column('owner', sa.String(length=320), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False),
        sa.Column('result', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_tasks_id', 'tasks', ['id'], unique=False)

def downgrade():
    op.drop_table('tasks')

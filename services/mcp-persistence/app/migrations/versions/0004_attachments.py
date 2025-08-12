"""add attachments table

Revision ID: 0004_attachments
Revises: 0003_tasks
Create Date: 2025-08-12 00:00:00
"""

from alembic import op
import sqlalchemy as sa

revision = '0004_attachments'
down_revision = '0003_tasks'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'attachments',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('project_id', sa.Integer(), sa.ForeignKey('projects.id', ondelete='CASCADE'), nullable=False),
        sa.Column('original_name', sa.String(length=500), nullable=False),
        sa.Column('stored_path', sa.String(length=1000), nullable=False),
        sa.Column('content_type', sa.String(length=200), nullable=True),
        sa.Column('size_bytes', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )
    op.create_index('ix_attachments_project_id', 'attachments', ['project_id'], unique=False)


def downgrade():
    op.drop_index('ix_attachments_project_id', table_name='attachments')
    op.drop_table('attachments')



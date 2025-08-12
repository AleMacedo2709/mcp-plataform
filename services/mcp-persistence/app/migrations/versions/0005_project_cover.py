from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0005_project_cover'
down_revision = '0004_attachments'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'project_covers',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('project_id', sa.Integer(), sa.ForeignKey('projects.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('original_name', sa.String(length=500), nullable=False),
        sa.Column('stored_path', sa.String(length=1000), nullable=False),
        sa.Column('content_type', sa.String(length=200), nullable=True),
        sa.Column('size_bytes', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('project_covers')



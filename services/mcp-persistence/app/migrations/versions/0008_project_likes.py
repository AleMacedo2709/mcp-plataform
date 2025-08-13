from alembic import op
import sqlalchemy as sa

revision = '0008_project_likes'
down_revision = '0007_project_actions_and_new_fields'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'project_likes',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('project_id', sa.Integer(), sa.ForeignKey('projects.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('user_email', sa.String(length=320), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index('ix_project_likes_unique', 'project_likes', ['project_id', 'user_email'], unique=True)


def downgrade() -> None:
    op.drop_index('ix_project_likes_unique', table_name='project_likes')
    op.drop_table('project_likes')



from alembic import op
import sqlalchemy as sa

revision = '0010_cnmp_awards_and_drop_project_categoria'
down_revision = '0009_contacts_results'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Drop legacy column 'categoria' from projects if exists
    try:
        with op.batch_alter_table('projects') as batch_op:
            batch_op.drop_column('categoria')
    except Exception:
        pass

    # Create awards table
    op.create_table(
        'project_cnmp_awards',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('project_id', sa.Integer(), sa.ForeignKey('projects.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('ano', sa.String(length=10), nullable=False),
        sa.Column('categoria', sa.String(length=100), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    )


def downgrade() -> None:
    op.drop_table('project_cnmp_awards')
    # cannot safely re-add old column on downgrade



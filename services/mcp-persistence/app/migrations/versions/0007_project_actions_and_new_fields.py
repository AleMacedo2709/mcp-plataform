from alembic import op
import sqlalchemy as sa

revision = '0007_project_actions_and_new_fields'
down_revision = '0006_project_members'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # New columns on projects
    op.add_column('projects', sa.Column('unidade_gestora', sa.String(length=200), nullable=True))
    op.add_column('projects', sa.Column('selo', sa.String(length=50), nullable=True))

    # New table project_actions
    op.create_table(
        'project_actions',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('project_id', sa.Integer(), sa.ForeignKey('projects.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('descricao', sa.String(length=1000), nullable=False),
        sa.Column('area_responsavel', sa.String(length=300), nullable=True),
        sa.Column('email_responsavel', sa.String(length=320), nullable=True),
        sa.Column('progresso', sa.String(length=50), nullable=True),
        sa.Column('inicio_previsto', sa.String(length=50), nullable=True),
        sa.Column('termino_previsto', sa.String(length=50), nullable=True),
        sa.Column('inicio_efetivo', sa.String(length=50), nullable=True),
        sa.Column('termino_efetivo', sa.String(length=50), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    )


def downgrade() -> None:
    op.drop_table('project_actions')
    op.drop_column('projects', 'selo')
    op.drop_column('projects', 'unidade_gestora')



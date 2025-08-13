from alembic import op
import sqlalchemy as sa

revision = '0009_contacts_results'
down_revision = '0008_project_likes'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Remove columns if exist (safe guard)
    with op.batch_alter_table('projects') as batch_op:
        try:
            batch_op.drop_column('contatos')
        except Exception:
            pass
        try:
            batch_op.drop_column('comprovacao_dos_resultados')
        except Exception:
            pass

    op.create_table(
        'project_contacts',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('project_id', sa.Integer(), sa.ForeignKey('projects.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('nome', sa.String(length=200), nullable=False),
        sa.Column('email', sa.String(length=320), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    )

    op.create_table(
        'project_result_proofs',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('project_id', sa.Integer(), sa.ForeignKey('projects.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('data_da_coleta', sa.String(length=50), nullable=True),
        sa.Column('resultado', sa.String(length=200), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    )


def downgrade() -> None:
    op.drop_table('project_result_proofs')
    op.drop_table('project_contacts')
    # cannot safely re-add old columns; skipping



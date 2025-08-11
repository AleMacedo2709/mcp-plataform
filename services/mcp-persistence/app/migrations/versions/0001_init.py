"""initial schema from CSV

Revision ID: 0001_init
Revises: 
Create Date: 2025-08-11 00:00:00

"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0001_init'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'projects',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('nome_da_iniciativa', sa.String(length=300), nullable=False),
        sa.Column('tipo_de_iniciativa', sa.String(), nullable=True),
        sa.Column('classificacao', sa.String(), nullable=True),
        sa.Column('natureza_da_iniciativa', sa.String(length=100), nullable=True),
        sa.Column('iniciativa_vinculada', sa.String(length=300), nullable=True),
        sa.Column('objetivo_estrategico_pen_mp', sa.String(), nullable=True),
        sa.Column('programa_pen_mp', sa.String(), nullable=True),
        sa.Column('promocao_do_objetivo_estrategico', sa.String(length=100), nullable=True),
        sa.Column('data_inicial_de_operacao', sa.String(length=300), nullable=True),
        sa.Column('fase_de_implementacao', sa.String(), nullable=True),
        sa.Column('descricao', sa.String(length=1000), nullable=False),
        sa.Column('estimativa_de_recursos', sa.String(length=200), nullable=True),
        sa.Column('publico_impactado', sa.String(length=100), nullable=True),
        sa.Column('orgaos_envolvidos', sa.String(length=200), nullable=True),
        sa.Column('contatos', sa.String(length=200), nullable=True),
        sa.Column('desafio_1', sa.String(length=300), nullable=True),
        sa.Column('desafio_2', sa.String(length=300), nullable=True),
        sa.Column('desafio_3', sa.String(length=300), nullable=True),
        sa.Column('resolutividade', sa.String(length=300), nullable=True),
        sa.Column('inovacao', sa.String(length=300), nullable=True),
        sa.Column('transparencia', sa.String(length=300), nullable=True),
        sa.Column('proatividade', sa.String(length=300), nullable=True),
        sa.Column('cooperacao', sa.String(length=300), nullable=True),
        sa.Column('resultado_1', sa.String(length=300), nullable=True),
        sa.Column('resultado_2', sa.String(length=300), nullable=True),
        sa.Column('resultado_3', sa.String(length=300), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    )

def downgrade():
    op.drop_table('projects')

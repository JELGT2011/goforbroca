"""add source to standard_deck

Revision ID: d79872842061
Revises: 55c91487523b
Create Date: 2020-03-04 00:50:03.071360

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'd79872842061'
down_revision = '55c91487523b'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('standard_decks', sa.Column('source', sa.String(length=256), nullable=True))
    op.create_index(op.f('ix_standard_decks_source'), 'standard_decks', ['source'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_standard_decks_source'), table_name='standard_decks')
    op.drop_column('standard_decks', 'source')

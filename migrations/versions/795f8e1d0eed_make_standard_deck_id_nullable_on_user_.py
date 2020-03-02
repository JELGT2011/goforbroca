"""make standard_deck_id nullable on user_deck

Revision ID: 795f8e1d0eed
Revises: e1d6fd137cde
Create Date: 2020-03-01 18:06:36.526085

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '795f8e1d0eed'
down_revision = 'e1d6fd137cde'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('user_decks', 'standard_deck_id', existing_type=sa.INTEGER(), nullable=True)


def downgrade():
    op.alter_column('user_decks', 'standard_deck_id', existing_type=sa.INTEGER(), nullable=False)

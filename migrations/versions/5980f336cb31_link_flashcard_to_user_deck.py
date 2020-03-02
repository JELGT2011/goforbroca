"""link flashcard to user_deck

Revision ID: 5980f336cb31
Revises: 795f8e1d0eed
Create Date: 2020-03-01 23:11:21.603272

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '5980f336cb31'
down_revision = '795f8e1d0eed'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('flashcards', 'standard_deck_id', existing_type=sa.INTEGER(), nullable=True)
    op.add_column('flashcards', sa.Column('user_deck_id', sa.Integer(), nullable=True))
    sa.ForeignKeyConstraint(('user_deck_id', ), ['user_decks.id'])


def downgrade():
    op.alter_column('flashcards', 'standard_deck_id', existing_type=sa.INTEGER(), nullable=False)
    op.drop_column('flashcards', 'user_deck_id')
    op.drop_constraint('user_deck_id', 'flashcards', type_='foreignkey')

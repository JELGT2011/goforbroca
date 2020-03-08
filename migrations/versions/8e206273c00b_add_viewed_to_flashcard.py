"""add viewed to flashcard

Revision ID: 8e206273c00b
Revises: 36e303213dda
Create Date: 2020-03-07 16:21:34.923230

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '8e206273c00b'
down_revision = '36e303213dda'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('flashcards', sa.Column('viewed', sa.Boolean(), nullable=True))


def downgrade():
    op.drop_column('flashcards', 'viewed')

"""add max_score to flashcard

Revision ID: 6102ac04a536
Revises: d79872842061
Create Date: 2020-03-04 20:40:09.897461

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '6102ac04a536'
down_revision = 'd79872842061'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('flashcards', sa.Column('max_score', sa.Float(), nullable=True))


def downgrade():
    op.drop_column('flashcards', 'max_score')

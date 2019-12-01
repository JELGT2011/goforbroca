"""create translations table

Revision ID: 525eb3b9d08c
Revises: 377263df5a46
Create Date: 2019-11-30 22:29:06.018010

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '525eb3b9d08c'
down_revision = '377263df5a46'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'translations',
        sa.Column('id', postgresql.UUID(), primary_key=True),

        sa.Column('from_language_id', postgresql.UUID(), sa.ForeignKey('languages.id')),
        sa.Column('to_language_id', postgresql.UUID(), sa.ForeignKey('languages.id')),

        sa.Column('from_word_id', postgresql.UUID(), sa.ForeignKey('words.id')),
        sa.Column('to_word_id', postgresql.UUID(), sa.ForeignKey('words.id')),

        sa.Column('count', sa.Integer()),
    )


def downgrade():
    op.drop_table('translations')

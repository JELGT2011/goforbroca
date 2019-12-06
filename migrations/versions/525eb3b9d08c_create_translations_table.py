"""create translations table

Revision ID: 525eb3b9d08c
Revises: 377263df5a46
Create Date: 2019-11-30 22:29:06.018010

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '525eb3b9d08c'
down_revision = '377263df5a46'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'translations',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.func.now()),
        sa.Column('from_word_id', sa.Integer(), sa.ForeignKey('words.id'), nullable=False),
        sa.Column('to_word_id', sa.Integer(), sa.ForeignKey('words.id'), nullable=False),
        sa.Column('rank', sa.Integer()),
    )


def downgrade():
    op.drop_table('translations')

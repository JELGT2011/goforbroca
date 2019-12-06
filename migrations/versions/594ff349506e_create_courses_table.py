"""create courses table

Revision ID: 594ff349506e
Revises: 93a3f33ab9fc
Create Date: 2019-12-03 20:34:03.575700

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '594ff349506e'
down_revision = '525eb3b9d08c'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'courses',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.func.now()),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('language_id', sa.Integer(), sa.ForeignKey('languages.id'), nullable=False),
        sa.Column('words_per_week', sa.Integer(), nullable=False)
    )


def downgrade():
    op.drop_table('courses')

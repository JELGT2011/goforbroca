"""create courses table

Revision ID: 93a3f33ab9fc
Revises: 594ff349506e
Create Date: 2019-12-03 20:34:03.575700

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '93a3f33ab9fc'
down_revision = '594ff349506e'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'courses',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.column('updated_at', sa.DateTime(timezone=True)),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('language_id', sa.Integer(), sa.ForeignKey('languages.id'), nullable=False),
        sa.Column('words_per_week', sa.Integer(), nullable=False)
    )


def downgrade():
    op.drop_table('courses')

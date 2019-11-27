"""empty message

Revision ID: 003b89127d7b
Revises: 
Create Date: 2019-11-26 23:02:55.914258

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '003b89127d7b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'language',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(length=255), unique=True, nullable=False)
    )


def downgrade():
    op.drop_table('language')

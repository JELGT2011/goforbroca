"""Adding user table

Revision ID: f098da0d31aa
Revises: 003b89127d7b
Create Date: 2019-11-27 11:49:55.064222

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.databases import postgresql


# revision identifiers, used by Alembic.
revision = 'f098da0d31aa'
down_revision = '003b89127d7b'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', postgresql.UUID(), primary_key=True),
        sa.Column('phone_number', sa.String(length=16), unique=True, nullable=False),
    )


def downgrade():
    op.drop_table('users')

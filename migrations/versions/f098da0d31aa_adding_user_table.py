"""Adding user table

Revision ID: f098da0d31aa
Revises: 003b89127d7b
Create Date: 2019-11-27 11:49:55.064222

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as PostgresDialect


# revision identifiers, used by Alembic.
revision = 'f098da0d31aa'
down_revision = '003b89127d7b'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', PostgresDialect.UUID(), primary_key=True),
        sa.Column('name', sa.String(length=255), unique=True, nullable=False),
        sa.Column('user_id', sa.String(length=50), unique=True, nullable=False),
    )


def downgrade():
    op.drop_table('users')

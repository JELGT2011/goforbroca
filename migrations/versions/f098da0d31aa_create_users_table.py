"""create users table

Revision ID: f098da0d31aa
Revises: 003b89127d7b
Create Date: 2019-11-27 11:49:55.064222

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'f098da0d31aa'
down_revision = '003b89127d7b'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.func.now()),
        sa.Column('phone_number', sa.String(length=16), unique=True, nullable=False),
    )


def downgrade():
    op.drop_table('users')

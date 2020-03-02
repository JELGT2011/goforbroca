"""add google_id to user

Revision ID: e1d6fd137cde
Revises: 36e303213dda
Create Date: 2020-02-29 23:36:06.751010

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'e1d6fd137cde'
down_revision = '36e303213dda'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column('google_id', sa.String(length=32), nullable=True))
    op.drop_constraint('users_phone_number_key', table_name='users')
    op.drop_column('users', 'phone_number')
    op.create_index(op.f('ix_users_google_id'), 'users', ['google_id'], unique=True)


def downgrade():
    op.drop_index(op.f('ix_users_google_id'), table_name='users')
    op.drop_column('users', 'google_id')
    op.add_column('users', sa.Column('phone_number', sa.String(length=16), nullable=False))

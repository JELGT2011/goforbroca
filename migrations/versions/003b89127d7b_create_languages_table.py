"""create languages table

Revision ID: 003b89127d7b
Revises: 
Create Date: 2019-11-26 23:02:55.914258

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '003b89127d7b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'languages',
        sa.Column('id', postgresql.UUID(), primary_key=True),
        sa.Column('name', sa.String(length=256), unique=True, nullable=False),
    )


def downgrade():
    op.drop_table('language')

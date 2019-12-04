"""create languages table

Revision ID: 003b89127d7b
Revises: 
Create Date: 2019-11-26 23:02:55.914258

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '003b89127d7b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'languages',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.column('updated_at', sa.DateTime(timezone=True)),
        sa.Column('name', sa.String(length=256), unique=True, nullable=False),
    )


def downgrade():
    op.drop_table('language')

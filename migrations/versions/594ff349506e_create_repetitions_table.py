"""create repetitions table

Revision ID: 594ff349506e
Revises: 525eb3b9d08c
Create Date: 2019-12-03 20:33:49.426948

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
        'repetitions',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.column('updated_at', sa.DateTime(timezone=True)),
        sa.Column('iteration', sa.Integer()),
        sa.Column('score', sa.Float()),
        sa.column('completed_at', sa.DateTime(timezone=True)),
    )


def downgrade():
    op.drop_table('repetitions')

"""create words table

Revision ID: 377263df5a46
Revises: f098da0d31aa
Create Date: 2019-11-30 22:19:45.336894

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '377263df5a46'
down_revision = 'f098da0d31aa'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'words',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('language_id', sa.Integer(), sa.ForeignKey('languages.id'), nullable=False),
        sa.Column('name', sa.String(256), index=True, nullable=False),
        sa.Column('pronunciation', sa.String(256)),
        sa.Column('etymology', sa.Text()),
        sa.Column('definition', sa.Text()),
    )


def downgrade():
    op.drop_table('words')

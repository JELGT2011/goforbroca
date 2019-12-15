"""create tables

Revision ID: 36e303213dda
Revises: 
Create Date: 2019-12-15 14:39:17.761151

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '36e303213dda'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'standard_decks',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('name', sa.String(length=256), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('phone_number', sa.String(length=16), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('phone_number'),
    )
    op.create_table(
        'flashcards',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('standard_deck_id', sa.Integer(), nullable=False),
        sa.Column('front', sa.String(length=1024), nullable=False),
        sa.Column('back', sa.String(length=1024), nullable=False),
        sa.Column('rank', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(('standard_deck_id', ), ['standard_decks.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_table(
        'user_decks',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('name', sa.String(length=256), nullable=False),
        sa.Column('standard_deck_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('active', sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(('standard_deck_id', ), ['standard_decks.id']),
        sa.ForeignKeyConstraint(('user_id', ), ['users.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_table(
        'repetitions',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('user_deck_id', sa.Integer(), nullable=False),
        sa.Column('flashcard_id', sa.Integer(), nullable=False),
        sa.Column('iteration', sa.Integer(), nullable=False),
        sa.Column('active', sa.Boolean(), nullable=False),
        sa.Column('score', sa.Float(), nullable=True),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(('flashcard_id', ), ['flashcards.id']),
        sa.ForeignKeyConstraint(('user_deck_id', ), ['user_decks.id']),
        sa.ForeignKeyConstraint(('user_id', ), ['users.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('repetitions')
    op.drop_table('user_decks')
    op.drop_table('flashcards')
    op.drop_table('users')
    op.drop_table('standard_decks')
    # ### end Alembic commands ###

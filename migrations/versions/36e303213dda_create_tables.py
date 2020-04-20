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
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), autoincrement=True, primary_key=True, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('email_address', sa.String(256), nullable=False, unique=True, index=True),
        sa.Column('google_id', sa.String(64), nullable=True, unique=True, index=True),
        sa.Column('facebook_id', sa.String(64), nullable=True, unique=True, index=True),
    )

    op.create_table(
        'languages',
        sa.Column('id', sa.Integer(), autoincrement=True, primary_key=True, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('name', sa.String(128), nullable=False, unique=True),
        sa.Column('locale', sa.String(64), nullable=False, unique=True),
    )

    op.create_table(
        'standard_decks',
        sa.Column('id', sa.Integer(), autoincrement=True, primary_key=True, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('name', sa.String(256), nullable=False),
        sa.Column('source', sa.String(256), nullable=False, index=True),
    )

    op.create_table(
        'user_decks',
        sa.Column('id', sa.Integer(), autoincrement=True, primary_key=True, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('name', sa.String(256), nullable=False),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('standard_deck_id', sa.Integer(), sa.ForeignKey('standard_decks.id'), nullable=True),
        sa.Column('active', sa.Boolean(), nullable=False),
    )

    op.create_table(
        'flashcards',
        sa.Column('id', sa.Integer(), autoincrement=True, primary_key=True, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('language_id', sa.Integer(), sa.ForeignKey('languages.id'), nullable=True),
        sa.Column('standard_deck_id', sa.Integer(), sa.ForeignKey('standard_decks.id'), nullable=True),
        sa.Column('user_deck_id', sa.Integer(), sa.ForeignKey('user_decks.id'), nullable=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('front', sa.String(1024), nullable=False),
        sa.Column('back', sa.String(1024), nullable=False),
        sa.Column('rank', sa.Integer(), nullable=True),
        sa.Column('audio_url', sa.String(1024), nullable=True),
        sa.Column('refresh_at', sa.DateTime(timezone=True), nullable=True),
    )

    op.create_table(
        'repetitions',
        sa.Column('id', sa.Integer(), autoincrement=True, primary_key=True, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('user_deck_id', sa.Integer(), sa.ForeignKey('user_decks.id'), nullable=False),
        sa.Column('flashcard_id', sa.Integer(), sa.ForeignKey('flashcards.id'), nullable=False),
        sa.Column('iteration', sa.Integer(), nullable=False),
        sa.Column('active', sa.Boolean(), nullable=False),
        sa.Column('score', sa.Integer(), nullable=True),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
    )


def downgrade():
    op.drop_table('repetitions')
    op.drop_table('flashcards')
    op.drop_table('user_decks')
    op.drop_table('standard_decks')
    op.drop_table('languages')
    op.drop_table('users')

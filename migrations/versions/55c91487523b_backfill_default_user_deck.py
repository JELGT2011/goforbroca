"""backfill default user_deck

Revision ID: 55c91487523b
Revises: 5980f336cb31
Create Date: 2020-03-04 00:43:47.844851

"""

from goforbroca.models.deck import UserDeck, default_deck_name
from goforbroca.models.user import User


# revision identifiers, used by Alembic.
revision = '55c91487523b'
down_revision = '5980f336cb31'
branch_labels = None
depends_on = None


def upgrade():
    for user in User.query.all():
        UserDeck.create_default_deck(user.id)


def downgrade():
    [default_user_deck.delete() for default_user_deck in UserDeck.query.filter_by(name=default_deck_name)]

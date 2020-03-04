from sqlalchemy import ForeignKey

from goforbroca.extensions import db
from goforbroca.models.base import Base

default_deck_name = 'My Vocabulary'


class StandardDeck(Base):
    __tablename__ = 'standard_decks'

    name = db.Column(db.String(256), nullable=False)


class UserDeck(Base):
    __tablename__ = 'user_decks'

    name = db.Column(db.String(256), nullable=False)
    standard_deck_id = db.Column(db.Integer(), ForeignKey('standard_decks.id'), nullable=True)
    user_id = db.Column(db.Integer(), ForeignKey('users.id'), nullable=False)
    active = db.Column(db.Boolean(), nullable=False)

    @classmethod
    def create_default_deck(cls, user_id: str) -> 'UserDeck':
        return UserDeck.create(
            name=default_deck_name,
            standard_deck_id=None,
            user_id=user_id,
            active=True,
        )

from sqlalchemy import ForeignKey

from goforbroca.extensions import db
from goforbroca.models.base import Base
from goforbroca.models.user import User

default_deck_name = 'My Vocabulary'
default_standard_deck_max_rank = 1000


class StandardDeck(Base):
    __tablename__ = 'standard_decks'

    name = db.Column(db.String(256), nullable=False)
    source = db.Column(db.String(256), nullable=True, index=True)


class UserDeck(Base):
    __tablename__ = 'user_decks'

    name = db.Column(db.String(256), nullable=False)
    user_id = db.Column(db.Integer(), ForeignKey(User.id, ondelete='CASCADE'), nullable=False)
    standard_deck_id = db.Column(db.Integer(), ForeignKey(StandardDeck.id), nullable=True)
    active = db.Column(db.Boolean(), nullable=False)

    @classmethod
    def create_default_deck(cls, user_id: str) -> 'UserDeck':
        return UserDeck.create(
            name=default_deck_name,
            standard_deck_id=None,
            user_id=user_id,
            active=True,
        )


class ForkedUserDeck(Base):
    __tablename__ = 'forked_user_decks'

    name = db.Column(db.String(256), nullable=False)
    user_id = db.Column(db.Integer(), ForeignKey(User.id, ondelete='CASCADE'), nullable=False)
    author_id = db.Column(db.Integer(), ForeignKey(User.id, ondelete='CASCADE'), nullable=False)
    standard_deck_id = db.Column(db.Integer(), ForeignKey(StandardDeck.id), nullable=True)
    active = db.Column(db.Boolean(), nullable=False)


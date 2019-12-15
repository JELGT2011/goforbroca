from sqlalchemy import ForeignKey

from goforbroca.extensions import db
from goforbroca.models.base import Base


class StandardDeck(Base):
    __tablename__ = 'standard_decks'

    name = db.Column(db.String(256), nullable=False)


class UserDeck(Base):
    __tablename__ = 'user_decks'

    name = db.Column(db.String(256), nullable=False)
    standard_deck_id = db.Column(db.Integer(), ForeignKey('standard_decks.id'), nullable=False)
    user_id = db.Column(db.Integer(), ForeignKey('users.id'), nullable=False)
    active = db.Column(db.Boolean(), nullable=False)

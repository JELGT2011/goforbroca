from sqlalchemy import ForeignKey

from goforbroca.extensions import db
from goforbroca.models.base import Base


class Flashcard(Base):
    __tablename__ = 'flashcards'

    standard_deck_id = db.Column(db.Integer(), ForeignKey('standard_decks.id'), nullable=False)
    front = db.Column(db.String(1024), nullable=False)
    back = db.Column(db.String(1024), nullable=False)
    rank = db.Column(db.Integer())

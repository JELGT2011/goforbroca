from sqlalchemy import ForeignKey

from goforbroca.extensions import db
from goforbroca.models.base import Base


class Flashcard(Base):
    __tablename__ = 'flashcards'

    standard_deck_id = db.Column(db.Integer(), ForeignKey('standard_decks.id'), nullable=True)
    user_deck_id = db.Column(db.Integer(), ForeignKey('user_decks.id'), nullable=True)
    user_id = db.Column(db.Integer(), ForeignKey('users.id'), nullable=True)
    front = db.Column(db.String(1024), nullable=False)
    back = db.Column(db.String(1024), nullable=False)
    rank = db.Column(db.Integer(), nullable=True)
    viewed = db.Column(db.Boolean(), nullable=True)
    progress = db.Column(db.Float(), nullable=True)

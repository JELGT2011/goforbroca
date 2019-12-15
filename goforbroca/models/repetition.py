from sqlalchemy import ForeignKey

from goforbroca.extensions import db
from goforbroca.models.base import Base


class Repetition(Base):
    __tablename__ = 'repetitions'

    user_id = db.Column(db.Integer(), ForeignKey('users.id'), nullable=False)
    user_deck_id = db.Column(db.Integer(), ForeignKey('user_decks.id'), nullable=False)
    flashcard_id = db.Column(db.Integer(), ForeignKey('flashcards.id'), nullable=False)
    iteration = db.Column(db.Integer(), nullable=False)
    active = db.Column(db.Boolean(), nullable=False)
    score = db.Column(db.Float())
    completed_at = db.Column(db.DateTime(timezone=True))

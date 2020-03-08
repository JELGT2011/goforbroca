from enum import Enum

from sqlalchemy import ForeignKey

from goforbroca.extensions import db
from goforbroca.models.base import Base


class RepetitionFormat(Enum):
    recognize = 'recognize'
    retrieve = 'retrieve'
    recall = 'recall'


class Repetition(Base):
    __tablename__ = 'repetitions'

    user_id = db.Column(db.Integer(), ForeignKey('users.id'), nullable=False)
    user_deck_id = db.Column(db.Integer(), ForeignKey('user_decks.id'), nullable=False)
    flashcard_id = db.Column(db.Integer(), ForeignKey('flashcards.id'), nullable=False)
    iteration = db.Column(db.Integer(), nullable=False)
    active = db.Column(db.Boolean(), nullable=False)
    format = db.Column(db.Enum(RepetitionFormat), nullable=False)
    prompt = db.Column(db.JSON(), nullable=False)
    answer = db.Column(db.String(128), nullable=False)
    attempt = db.Column(db.String(128), nullable=True)
    score = db.Column(db.Float(), nullable=True)
    completed_at = db.Column(db.DateTime(timezone=True))

    def generate_prompt(self) -> 'Repetition':
        raise NotImplementedError()

from sqlalchemy import ForeignKey

from goforbroca.extensions import db
from goforbroca.models.base import Base
from goforbroca.models.deck import UserDeck
from goforbroca.models.flashcard import Flashcard
from goforbroca.models.user import User


class Repetition(Base):
    __tablename__ = 'repetitions'

    user_id = db.Column(db.Integer(), ForeignKey(User.id), nullable=False)
    user_deck_id = db.Column(db.Integer(), ForeignKey(UserDeck.id), nullable=False)
    flashcard_id = db.Column(db.Integer(), ForeignKey(Flashcard.id), nullable=False)
    iteration = db.Column(db.Integer(), nullable=False)
    active = db.Column(db.Boolean(), nullable=False)
    score = db.Column(db.Integer(), nullable=True)
    completed_at = db.Column(db.DateTime(timezone=True), nullable=True)

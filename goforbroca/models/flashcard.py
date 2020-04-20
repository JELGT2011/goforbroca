from sqlalchemy import ForeignKey

from goforbroca.extensions import db
from goforbroca.models.base import Base
from goforbroca.models.deck import StandardDeck, UserDeck
from goforbroca.models.language import Language
from goforbroca.models.user import User


class Flashcard(Base):
    __tablename__ = 'flashcards'

    language_id = db.Column(db.Integer(), ForeignKey(Language.id), nullable=True)
    standard_deck_id = db.Column(db.Integer(), ForeignKey(StandardDeck.id), nullable=True)
    user_deck_id = db.Column(db.Integer(), ForeignKey(UserDeck.id), nullable=True)
    user_id = db.Column(db.Integer(), ForeignKey(User.id), nullable=True)
    front = db.Column(db.String(1024), nullable=False)
    back = db.Column(db.String(1024), nullable=False)
    rank = db.Column(db.Integer(), nullable=True)
    audio_url = db.Column(db.String(1024), nullable=True)
    refresh_at = db.Column(db.DateTime(timezone=True), nullable=True)

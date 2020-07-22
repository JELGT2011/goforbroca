from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey

from goforbroca.extensions import db
from goforbroca.models.base import Base
from goforbroca.models.deck import StandardDeck, UserDeck, default_deck_name
from goforbroca.models.language import Language
from goforbroca.models.user import User
from goforbroca.util.audio import create_and_store_tts
from goforbroca.util.google import translate_text


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

    @classmethod
    def create_from_user_data(
            cls,
            user: User,
            language: Language,
            front: str,
            back: Optional[str] = None,
            rank: Optional[int] = None,
            audio_url: Optional[str] = None,
            user_deck_id: Optional[int] = None,
    ) -> 'Flashcard':

        # TODO: support translating to languages other than English
        if back is None:
            back = translate_text(front, 'en')

        if audio_url is None:
            audio_url = create_and_store_tts(front, language.locale)

        if user_deck_id is None:
            user_deck_id = UserDeck.query.filter_by(user_id=user.id, name=default_deck_name).scalar().id

        flashcard = Flashcard.create(
            language_id=language.id,
            user_deck_id=user_deck_id,
            user_id=user.id,
            front=front,
            back=back,
            rank=rank,
            audio_url=audio_url,
            refresh_at=datetime.utcnow(),
        )
        return flashcard

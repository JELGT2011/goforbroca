from sqlalchemy import ForeignKey

from goforbroca.extensions import db
from goforbroca.models.base import Base


class Translations(Base):
    from_word_id = db.Column(db.Integer(), ForeignKey('words.id'), nullable=False)
    to_word_id = db.Column(db.Integer(), ForeignKey('words.id'), nullable=False)
    rank = db.Column(db.Integer())

from sqlalchemy import ForeignKey
from sqlalchemy.dialects import postgresql

from goforbroca.extensions import db
from goforbroca.models.base import Base


class Translations(Base):
    from_language_id = db.Column(postgresql.UUID(), ForeignKey('languages.id'))
    to_language_id = db.Column(postgresql.UUID(), ForeignKey('languages.id'))

    from_word_id = db.Column(postgresql.UUID(), ForeignKey('words.id'))
    to_word_id = db.Column(postgresql.UUID(), ForeignKey('words.id'))

    count = db.Column(db.Integer())

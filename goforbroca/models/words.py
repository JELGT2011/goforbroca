from typing import Optional

from sqlalchemy import ForeignKey

from goforbroca.extensions import db
from goforbroca.models.base import Base


class Words(Base):
    language_id = db.Column(db.Integer(), ForeignKey('languages.id'), nullable=False)
    name = db.Column(db.String(256), index=True, nullable=False)
    pronunciation = db.Column(db.String(256))
    etymology = db.Column(db.Text())
    definition = db.Column(db.Text())

    @classmethod
    def get_by_name(cls, name: str) -> Optional['Words']:
        return db.session.query(Words).filter_by(name=name).first()

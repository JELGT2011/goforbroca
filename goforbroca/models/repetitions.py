from sqlalchemy import ForeignKey

from goforbroca.extensions import db
from goforbroca.models.base import Base


class Repetitions(Base):
    translation_id = db.Column(db.Integer(), ForeignKey('translations.id'), nullable=False)
    iteration = db.Column(db.Integer(), nullable=False)
    score = db.Column(db.Float())
    completed_at = db.Column(db.DateTime(timezone=True))

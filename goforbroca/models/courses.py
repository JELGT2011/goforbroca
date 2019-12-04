from sqlalchemy import ForeignKey

from goforbroca.extensions import db
from goforbroca.models.base import Base


class Courses(Base):
    user_id = db.Column(db.Integer(), ForeignKey('users.id'), nullable=False)
    language_id = db.Column(db.Integer(), ForeignKey('languages.id'), nullable=False)
    words_per_week = db.Column(db.Integer(), nullable=False)

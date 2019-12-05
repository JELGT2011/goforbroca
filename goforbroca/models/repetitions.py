from datetime import datetime

from sqlalchemy import ForeignKey

from goforbroca.extensions import db
from goforbroca.models.base import Base


class Repetitions(Base):
    course_id = db.Column(db.Integer(), ForeignKey('courses.id'), nullable=False)
    translation_id = db.Column(db.Integer(), ForeignKey('translations.id'), nullable=False)
    iteration = db.Column(db.Integer(), nullable=False)
    score = db.Column(db.Float())
    completed_at = db.Column(db.DateTime(timezone=True))

    @classmethod
    def new_words_this_week(cls, course_id: int) -> int:
        now = datetime.utcnow()
        last_week = now.replace(day=now.day - 7)
        return (db.session.query(Repetitions)
                .filter_by(course_id=course_id, created_at__gt=last_week)
                .group_by(Repetitions.translation_id)
                .count())

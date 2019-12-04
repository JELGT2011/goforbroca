from typing import Optional

from goforbroca.extensions import db
from goforbroca.models.base import Base


class Languages(Base):
    name = db.Column(db.String(256), unique=True, nullable=False)

    @classmethod
    def get_by_name(cls, name: str) -> Optional['Languages']:
        return db.session.query(Languages).filter_by(name=name).first()

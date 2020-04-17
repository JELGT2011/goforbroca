from goforbroca.extensions import db
from goforbroca.models.base import Base


class Language(Base):
    __tablename__ = 'languages'

    name = db.Column(db.String(1024), nullable=False, unique=True)
    locale = db.Column(db.String(64), nullable=False, unique=True)

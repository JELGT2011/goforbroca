from goforbroca.extensions import db
from goforbroca.models.base import Base


class Languages(Base):
    name = db.Column(db.String(256), unique=True, nullable=False)

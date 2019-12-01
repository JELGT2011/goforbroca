from goforbroca.extensions import db
from goforbroca.models.base import Base


class Users(Base):
    phone_number = db.Column(db.String(16), unique=True, nullable=False)

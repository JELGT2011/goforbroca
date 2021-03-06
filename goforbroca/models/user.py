from goforbroca.extensions import db
from goforbroca.models.base import Base


class User(Base):
    __tablename__ = 'users'

    email_address = db.Column(db.String(256), unique=True, nullable=False, index=True)
    google_id = db.Column(db.String(64), unique=True, nullable=True, index=True)
    facebook_id = db.Column(db.String(64), unique=True, nullable=True, index=True)
    sms_enabled = db.Column(db.Boolean(False), index=True)
    phone_number = db.Column(db.String(10), unique=True, index=True)

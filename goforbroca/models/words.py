from goforbroca.extensions import db
from goforbroca.models.base import Base


class Words(Base):
    name = db.Column(db.String(256), index=True)
    pronunciation = db.Column(db.String(256), nullable=True)
    etymology = db.Column(db.Text(), nullable=True)
    definition = db.Column(db.Text(), nullable=True)
    translation = db.relationship('Translations')

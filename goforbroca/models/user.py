from goforbroca.extensions import db
from goforbroca.models.base import Base


class User(Base):
    __tablename__ = 'users'

    google_id = db.Column(db.String(32), unique=True, nullable=True, index=True)

    def to_json(self):
        base = super().to_json()
        results = {
            'google_id': self.google_id,
            **base,
        }

        return results

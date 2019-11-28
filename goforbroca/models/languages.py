from sqlalchemy.dialects import postgresql

from goforbroca.extensions import db


class Language(db.Model):
    id = db.Column(postgresql.UUID(), primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)

    def __repr__(self):
        return f"<Language {self.id}: {self.name}>"

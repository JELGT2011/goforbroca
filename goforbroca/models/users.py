from sqlalchemy.databases import postgresql

from goforbroca.extensions import db


class User(db.Model):
    id = db.Column(postgresql.UUID(), primary_key=True)
    phone_number = db.Column(db.String(16), unique=True, nullable=False)

    def __repr__(self):
        return f"<User {self.id}: {self.phone_number}>"

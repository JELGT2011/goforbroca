from sqlalchemy.databases import postgresql

from goforbroca.extensions import db


class Base(db.Model):
    id = db.Column(postgresql.UUID(), primary_key=True)

    def __repr__(self):
        return f'<{self.__class__} {self.id}>: {self.__dict__}'

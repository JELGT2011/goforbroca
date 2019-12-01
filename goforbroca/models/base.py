from goforbroca.extensions import db


class Base(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)

    def __repr__(self):
        return f'<{self.__class__} {self.id}>: {self.__dict__}'

from typing import List

from goforbroca.extensions import db


class Base(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)

    def __repr__(self):
        return f'<{self.__class__} {self.id}>: {self.__dict__}'

    @classmethod
    def create(cls, **kwargs) -> 'Base':
        model = cls(**kwargs)
        db.session.add(model)
        db.session.commit()
        return model

    @classmethod
    def bulk_create(cls, data) -> List['Base']:
        models = list()
        for datum in data:
            model = cls(**datum)
            models.append(model)
            db.session.add(model)
        db.session.commit()
        return models

    @classmethod
    def all(cls) -> List['Base']:
        return db.session.query(cls).all()

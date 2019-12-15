from datetime import datetime
from typing import List

from sqlalchemy import func

from goforbroca.extensions import db


class Base(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

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

    def save(self) -> 'Base':
        self.updated_at = datetime.utcnow()
        db.session.add(self)
        db.session.commit()
        return self

    @classmethod
    def all(cls) -> List['Base']:
        return db.session.query(cls).all()

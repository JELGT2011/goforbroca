from datetime import datetime

from sqlalchemy import func

from goforbroca.extensions import db


class Base(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now(), nullable=True)

    def __repr__(self):
        return f'<{self.__class__} {self.id}>: {self.__dict__}'

    @classmethod
    def create(cls, **kwargs) -> 'Base':
        model = cls(**kwargs)
        db.session.add(model)
        db.session.commit()
        return model

    def save(self) -> 'Base':
        self.updated_at = datetime.utcnow()
        db.session.add(self)
        db.session.commit()
        return self

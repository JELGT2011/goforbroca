from goforbroca.extensions import db, PostgresDialect


class User(db.Model):
    id = db.Column(PostgresDialect.UUID(), primary_key=True)
    # TODO @libbey, migrate this to make name not unique, happens
    name = db.Column(db.String(255), unique=True, nullable=False)
    user_id = db.Column(db.String(50))

    def __repr__(self):
        return f"<User {self.name}: {self.user_id}>"

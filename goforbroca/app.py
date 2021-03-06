from celery.schedules import crontab
from flask import Flask
from flask_cors import CORS

from goforbroca.config import DEBUG, HOST
from goforbroca.extensions import db, migrate, celery


def create_app(testing=False, cli=False):
    """Application factory, used to create application
    """
    app = Flask('goforbroca')
    app.url_map.strict_slashes = False
    app.config.from_object('goforbroca.config')

    if testing is True:
        app.config['TESTING'] = True

    configure_cors(app)
    configure_extensions(app, cli)
    register_blueprints(app)
    init_celery(app)

    return app


def configure_cors(app):
    if DEBUG:
        cors = CORS(app, origin='*')
    else:
        cors = CORS(app, origin=HOST)
    return cors


def configure_extensions(app, cli):
    """configure flask extensions
    """
    db.init_app(app)

    if cli is True:
        migrate.init_app(app, db)


def register_blueprints(app):
    """register all blueprints for application
    """
    from goforbroca.api.deck import deck_blueprint
    from goforbroca.api.flashcard import flashcard_blueprint
    from goforbroca.api.repetition import repetition_blueprint
    from goforbroca.api.user import user_blueprint

    app.url_map.strict_slashes = False
    app.register_blueprint(deck_blueprint)
    app.register_blueprint(flashcard_blueprint)
    app.register_blueprint(repetition_blueprint)
    app.register_blueprint(user_blueprint)


def init_celery(app=None):
    app = app or create_app()
    celery.conf.broker_url = app.config['CELERY_BROKER_URL']
    celery.conf.result_backend = app.config['CELERY_RESULT_BACKEND']
    celery.conf.update(app.config)
    celery.conf.beat_schedule = {
        'learn-every-day': {
            'task': 'tasks.learn',
            'schedule': crontab(minute=0, hour=12),
        },
    }

    class ContextTask(celery.Task):
        """Make celery tasks work with Flask app context"""

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

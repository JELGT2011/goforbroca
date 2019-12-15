from flask import Flask

from goforbroca.extensions import db, migrate, celery


def create_app(testing=False, cli=False):
    """Application factory, used to create application
    """
    app = Flask('goforbroca')
    app.config.from_object('goforbroca.config')

    if testing is True:
        app.config['TESTING'] = True

    configure_extensions(app, cli)
    register_blueprints(app)
    init_celery(app)

    return app


def configure_extensions(app, cli):
    """configure flask extensions
    """
    db.init_app(app)

    if cli is True:
        migrate.init_app(app, db)


def register_blueprints(app):
    """register all blueprints for application
    """
    from goforbroca.api.sms import sms
    app.register_blueprint(sms)


def init_celery(app=None):
    app = app or create_app()
    celery.conf.broker_url = app.config['CELERY_BROKER_URL']
    celery.conf.result_backend = app.config['CELERY_RESULT_BACKEND']
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        """Make celery tasks work with Flask app context"""

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

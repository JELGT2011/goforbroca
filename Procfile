web: gunicorn goforbroca.wsgi:app
worker: celery worker --app=goforbroca.celery_app:app
release: goforbroca db upgrade

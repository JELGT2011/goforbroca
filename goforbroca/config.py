"""Default configuration

Use env var to override
"""
import os

ENV = os.environ["FLASK_ENV"]
DEBUG = ENV == "development"
SECRET_KEY = os.environ["SECRET_KEY"]

SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URI"]
SQLALCHEMY_TRACK_MODIFICATIONS = False

JWT_BLACKLIST_ENABLED = True
JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
CELERY_BROKER_URL = os.environ["CELERY_BROKER_URL"]
CELERY_RESULT_BACKEND = os.environ["CELERY_RESULT_BACKEND_URL"]
GOOGLE_CLIENT_ID = os.environ["GOOGLE_CLIENT_ID"]
GOOGLE_CLIENT_SECRET = os.environ["GOOGLE_CLIENT_SECRET"]

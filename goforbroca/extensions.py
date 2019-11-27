"""Extensions registry

All extensions here are used as singletons and
initialized in application factory
"""
from celery import Celery
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from passlib.context import CryptContext
import sqlalchemy.dialects.postgresql as PostgresDialect

db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()
pwd_context = CryptContext(schemes=['pbkdf2_sha256'], deprecated='auto')
celery = Celery()

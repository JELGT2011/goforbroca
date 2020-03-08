from functools import wraps
from typing import Optional, Callable

from flask import request, make_response
from google.auth.transport import requests
from google.oauth2 import id_token

from goforbroca.config import GOOGLE_CLIENT_ID
from goforbroca.models.user import User

google_auth_issuers = frozenset(['accounts.google.com', 'https://accounts.google.com'])


def get_authenticated_google_user_from_token(token: str) -> Optional[str]:
    try:
        id_info = id_token.verify_oauth2_token(token, requests.Request(), GOOGLE_CLIENT_ID)
        if id_info['iss'] not in google_auth_issuers:
            return None

        user_id = id_info['sub']  # ID token is valid. Get the user's Google Account ID from the decoded token.
        return user_id
    except ValueError:
        return None


def wrap_authenticated_user(wrapped: Callable) -> Callable:

    @wraps(wrapped)
    def func(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return make_response({'msg': 'authentication header required'}, 403)

        try:
            auth_token = auth_header.split()[1]
        except IndexError:
            return make_response({'msg': 'invalid auth header format'}, 403)

        google_id = get_authenticated_google_user_from_token(auth_token)
        if not google_id:
            return make_response({'msg': 'invalid google auth header'}, 403)

        user = User.query.filter_by(google_id=google_id).scalar()
        if not user:
            return make_response({'msg': 'user not found'}, 404)

        return wrapped(user, *args, **kwargs)

    return func


def wrap_google_user(wrapped: Callable) -> Callable:

    @wraps(wrapped)
    def func(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return make_response({'msg': 'authentication header required'}, 403)

        try:
            auth_token = auth_header.split()[1]
        except IndexError:
            return make_response({'msg': 'invalid auth header format'}, 403)

        google_id = get_authenticated_google_user_from_token(auth_token)
        if not google_id:
            return make_response({'msg': 'invalid google auth header'}, 403)

        return wrapped(google_id, *args, **kwargs)

    return func

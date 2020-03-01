from functools import wraps
from typing import Optional, Callable

from flask import Response, request
from google.auth.transport import requests
from google.oauth2 import id_token

from goforbroca.config import GOOGLE_CLIENT_ID

google_auth_issuers = frozenset(['accounts.google.com', 'https://accounts.google.com'])
google_auth_header = 'google-auth-token'


def get_authenticated_google_user_from_token(token: str) -> Optional[str]:
    try:
        id_info = id_token.verify_oauth2_token(token, requests.Request(), GOOGLE_CLIENT_ID)
        if id_info['iss'] not in google_auth_issuers:
            return None

        user_id = id_info['sub']  # ID token is valid. Get the user's Google Account ID from the decoded token.
        return user_id
    except ValueError:
        return None


def wrap_google_auth_user(wrapped: Callable) -> Callable:

    @wraps(wrapped)
    def func(*args, **kwargs):
        google_auth_token = request.headers.get(google_auth_header)
        google_id = get_authenticated_google_user_from_token(google_auth_token)
        if not google_id:
            return Response({'msg': 'invalid google auth header'}, 403)

        return wrapped(google_id, *args, **kwargs)

    return func

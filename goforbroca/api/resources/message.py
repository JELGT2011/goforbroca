import json

import requests
from flask import request, Response
from flask_restful import Resource


class MessageResource(Resource):

    @classmethod
    def post(cls) -> Response:
        return Response('EVENT RECEIVED')

    @classmethod
    def handle_message(cls, user_id, user_message):
        return f'Hello {user_id}! You just sent me: {user_message}'

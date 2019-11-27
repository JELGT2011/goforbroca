import json

import requests
from flask import request, Response
from flask_restful import Resource

from goforbroca.config import ACCESS_TOKEN, VERIFY_TOKEN


class MessageResource(Resource):

    @classmethod
    def get(cls) -> Response:
        if request.args.get('hub.verify_token') == VERIFY_TOKEN:
            hub_challenge = request.args.get('hub.challenge')
            return Response(hub_challenge)
        return Response('Wrong verify token')

    @classmethod
    def post(cls) -> Response:
        data = json.loads(request.data.decode('utf-8'))
        for entry in data['entry']:
            user_message = entry['messaging'][0]['message']['text']
            user_id = entry['messaging'][0]['sender']['id']
            response = {
                'recipient': {'id': user_id},
                'message': {},
            }
            response['message']['text'] = cls.handle_message(user_id, user_message)
            requests.post(f'https://graph.facebook.com/v2.6/me/messages/?access_token={ACCESS_TOKEN}', json=response)
        return Response('EVENT RECEIVED')

    @classmethod
    def handle_message(cls, user_id, user_message):
        return f'Hello {user_id}! You just sent me: {user_message}'

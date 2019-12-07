from flask import Response, request
from flask_restful import Resource
from twilio.twiml.messaging_response import MessagingResponse


class SMSResource(Resource):

    @classmethod
    def post(cls) -> Response:
        message_body = request.form['Body']
        response = MessagingResponse()
        response.message('the')
        return Response(response)

    @classmethod
    def handle_message(cls, user_id, user_message):
        return f'Hello {user_id}! You just sent me: {user_message}'

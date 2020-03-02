import re
from datetime import datetime

from flask import request, Blueprint
from strsimpy import NormalizedLevenshtein
from twilio.twiml.messaging_response import MessagingResponse

from goforbroca.extensions import db
from goforbroca.models.flashcard import Flashcard
from goforbroca.models.repetition import Repetition
from goforbroca.models.user import User

sms_blueprint = Blueprint('sms', __name__, url_prefix='/api/sms')

normalized_levenshtein = NormalizedLevenshtein()


def handle_help() -> str:
    return '\n'.join({'help', 'enroll', 'study'})


# TODO: tune this score calculation to understand time spent, and iteration number
# noinspection PyUnusedLocal
def calculate_score(repetition: Repetition, attempt: str, answer: str) -> float:
    distance = normalized_levenshtein.distance(attempt, answer)
    return distance


def handle_study(repetition: Repetition, message_body: str) -> str:
    flashcard = db.session.query(Flashcard).get(repetition.flashcard_id)
    score = calculate_score(repetition, message_body, flashcard.back)

    repetition.active = False
    repetition.score = score
    repetition.completed_at = datetime.utcnow()
    repetition.save()

    if score < 0.8:
        return f'sorry, that was not close enough to the answer: {flashcard.back}'
    return f'good job, the answer was: {flashcard.back}'


@sms_blueprint.route('/', methods=['POST'])
def post() -> str:
    message_body = request.form['Body']
    requester_phone_number = request.form['From']
    response = MessagingResponse()

    user = db.session.query(User).filter_by(phone_number=requester_phone_number).scalar()
    if not user:
        user = User.create(phone_number=requester_phone_number)

    active_repetition = db.session.query(Repetition).filter_by(user_id=user.id, active=True).scalar()
    if active_repetition:
        response_message = handle_study(active_repetition, message_body)
        response.message(response_message)
        return str(response)

    response_message = handle_help()
    response.message(response_message)
    return str(response)

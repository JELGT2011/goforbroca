import re
from datetime import datetime

from flask import Response, request, Blueprint
from strsimpy import NormalizedLevenshtein
from twilio.twiml.messaging_response import MessagingResponse

from goforbroca.extensions import db
from goforbroca.models.courses import Courses
from goforbroca.models.languages import Languages
from goforbroca.models.repetitions import Repetitions
from goforbroca.models.translations import Translations
from goforbroca.models.users import Users
from goforbroca.models.words import Words

sms = Blueprint('sms', __name__, url_prefix='/api/sms')

enroll_regex = re.compile(r'enroll (\w+)')
normalized_levenshtein = NormalizedLevenshtein()


def handle_help() -> str:
    return '\n'.join({'help', 'enroll', 'study'})


def handle_enroll(user: Users, language_name: str) -> str:
    language = db.session.query(Languages).filter_by(name=language_name).scalar()
    course = db.session.query(Courses).filter_by(user_id=user.id, language_id=language.id).scalar()
    if course:
        return f'you are already enrolled in {language.name}'
    else:
        Courses.create(user_id=user.id, language_id=language.id, words_per_week=7)
        return f'you have successfully enrolled in {language.name}'


# TODO: tune this score calculation to understand time spent, and iteration number
# noinspection PyUnusedLocal
def calculate_score(repetition: Repetitions, attempt: str, answer: str) -> float:
    distance = normalized_levenshtein.distance(attempt, answer)
    return distance


def handle_study(repetition: Repetitions, message_body: str) -> str:
    translation = db.session.query(Translations).get(repetition.translation_id)
    to_word = db.session.query(Words).get(translation.to_word_id)
    score = calculate_score(repetition, message_body, to_word.name)

    repetition.active = False
    repetition.score = score
    repetition.completed_at = datetime.utcnow()

    if score < 0.8:
        return f'sorry, that was not close enough to the answer: {to_word.name}'
    return f'good job, the answer was: {to_word.name}'


@sms.route('/', methods=['POST'])
def post() -> Response:
    message_body = request.form['Body']
    requester_phone_number = request.form['From']
    response = MessagingResponse()

    user = db.session.query(Users).filter_by(phone_number=requester_phone_number).scalar()
    if not user:
        user = Users.create(phone_number=requester_phone_number)

    match = enroll_regex.fullmatch(message_body)
    if match:
        language_name = match.group()
        response_message = handle_enroll(user, language_name)
        response.message(response_message)
        return Response(response)

    active_repetition = db.session.query(Repetitions).filter_by(user_id=user.id, active=True).scalar()
    if active_repetition:
        response_message = handle_study(active_repetition, message_body)
        response.message(response_message)
        return Response(response)

    response_message = handle_help()
    response.message(response_message)
    return Response(response)

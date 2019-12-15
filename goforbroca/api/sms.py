import re
from datetime import datetime

from flask import Response, request, Blueprint
from strsimpy import NormalizedLevenshtein
from twilio.twiml.messaging_response import MessagingResponse

from goforbroca.extensions import db
from goforbroca.models.deck import StandardDeck, UserDeck
from goforbroca.models.flashcard import Flashcard
from goforbroca.models.repetition import Repetition
from goforbroca.models.user import User

sms = Blueprint('sms', __name__, url_prefix='/api/sms')

enroll_regex = re.compile(r'enroll ?(\d*)')
normalized_levenshtein = NormalizedLevenshtein()


def handle_help() -> str:
    return '\n'.join({'help', 'enroll', 'study'})


def handle_enroll(user: User, standard_deck_id: str) -> str:
    if not standard_deck_id:
        # list all decks
        standard_decks = db.session.query(StandardDeck).all()
        return '\n'.join([f'{deck.id}: {deck.name}' for deck in standard_decks])

    standard_deck = db.session.query(StandardDeck).get(standard_deck_id)
    user_deck = db.session.query(UserDeck).filter_by(user_id=user.id, standard_dec_id=standard_deck.id).scalar()
    if user_deck:
        return f'you are already enrolled in {user_deck.name}'
    else:
        user_deck = UserDeck.create(
            name=standard_deck.name,
            standard_dec_id=standard_deck.id,
            user_id=user.id,
            active=True,
        )
        return f'you have successfully enrolled in {user_deck.name}'


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


@sms.route('/', methods=['POST'])
def post() -> Response:
    message_body = request.form['Body']
    requester_phone_number = request.form['From']
    response = MessagingResponse()

    user = db.session.query(User).filter_by(phone_number=requester_phone_number).scalar()
    if not user:
        user = User.create(phone_number=requester_phone_number)

    match = enroll_regex.fullmatch(message_body)
    if match:
        standard_deck_id = match.group()
        response_message = handle_enroll(user, standard_deck_id)
        response.message(response_message)
        return Response(response)

    active_repetition = db.session.query(Repetition).filter_by(user_id=user.id, active=True).scalar()
    if active_repetition:
        response_message = handle_study(active_repetition, message_body)
        response.message(response_message)
        return Response(response)

    response_message = handle_help()
    response.message(response_message)
    return Response(response)

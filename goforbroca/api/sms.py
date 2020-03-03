from datetime import datetime

from flask import Blueprint
from strsimpy import NormalizedLevenshtein

from goforbroca.extensions import db
from goforbroca.models.flashcard import Flashcard
from goforbroca.models.repetition import Repetition

sms_blueprint = Blueprint('sms', __name__, url_prefix='/api/sms')

normalized_levenshtein = NormalizedLevenshtein()


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


# def post() -> str:
#     active_repetition = db.session.query(Repetition).filter_by(user_id=user.id, active=True).scalar()
#     if active_repetition:
#         response_message = handle_study(active_repetition, message_body)
#         response.message(response_message)
#         return str(response)
#
#     return str(response)

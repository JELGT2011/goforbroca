from datetime import datetime

from flask import Blueprint, Response, make_response, request
from sqlalchemy import asc, or_
from strsimpy import NormalizedLevenshtein

from goforbroca.extensions import db, ma
from goforbroca.models.deck import UserDeck
from goforbroca.models.flashcard import Flashcard
from goforbroca.models.repetition import Repetition
from goforbroca.models.user import User
from goforbroca.util.auth import wrap_authenticated_user

min_learned_score = 0.95
normalized_levenshtein = NormalizedLevenshtein()

repetition_blueprint = Blueprint('repetition', __name__, url_prefix='/api/repetitions')


# TODO: tune this score calculation to understand time spent, and iteration number
def calculate_score(repetition: Repetition) -> float:
    distance = normalized_levenshtein.distance(repetition.attempt, repetition.answer)
    return distance


class RepetitionSchema(ma.ModelSchema):

    user_deck_id = ma.Int(dump_only=True)
    flashcard_id = ma.Int(dump_only=True)

    class Meta:
        model = Repetition
        sqla_session = db.session


repetition_schema = RepetitionSchema()


@repetition_blueprint.route('/', methods=['GET'])
@wrap_authenticated_user
def create_repetition(user: User) -> Response:
    user_deck_ids = {user_deck.id for user_deck in UserDeck.query.filter_by(user_id=user.id)}

    user_deck_id = request.json.get('user_deck_id')
    if user_deck_id:
        if user_deck_id not in user_deck_ids:
            return make_response({"msg": "invalid user_deck_id"}, 400)

        flashcard = (Flashcard.query
                     .filter(Flashcard.user_deck_id == user_deck_id)
                     .filter(Flashcard.viewed.is_(True))
                     .filter(or_(Flashcard.max_score < min_learned_score, Flashcard.max_score.is_(None)))
                     .order_by(asc(Flashcard.rank))
                     .limit(1).scalar())
    else:
        flashcard = (Flashcard.query
                     .filter(Flashcard.user_deck_id.in_(user_deck_ids))
                     .filter(Flashcard.viewed.is_(True))
                     .filter(or_(Flashcard.max_score < min_learned_score, Flashcard.max_score.is_(None)))
                     .order_by(asc(Flashcard.rank))
                     .limit(1).scalar())

    if not flashcard:
        return make_response({"msg": "no flashcards to review"}, 200)

    # TODO: find previous repetition if it exists (to calibrate and set iteration number)
    previous = Repetition.query.filter_by(flashcard_id=flashcard.id)
    active = [repetition.active for repetition in previous]
    if active:
        last_active = max(active, key=lambda repetition: repetition.created_at)
        return make_response({"repetition": repetition_schema.dump(last_active).data}, 200)

    latest = max(previous, key=lambda repetition: repetition.iteration)
    repetition = Repetition.create(
        user_deck_id=flashcard.user_deck_id,
        flashcard_id=flashcard.id,
        iteration=latest.iteration + 1,
        active=True,
        score=None,
    )

    return make_response({"repetition": repetition_schema.dump(repetition).data}, 200)


@repetition_blueprint.route('/<repetition_id>', methods=['POST'])
@wrap_authenticated_user
def submit_repetition_answer(user: User, repetition_id: int) -> Response:
    attempt = request.json['attempt']

    repetition = Repetition.query.filter_by(id=repetition_id, user_id=user.id, active=True).scalar()
    if not repetition:
        return make_response({"msg": "repetition not found"}, 404)

    flashcard = Flashcard.query.filter_by(id=repetition.flashcard_id).scalar()
    if not flashcard:
        return make_response({"msg": "flashcard not found"}, 404)

    repetition.active = False
    repetition.attempt = attempt
    repetition.score = calculate_score(repetition)
    repetition.completed_at = datetime.utcnow()
    repetition.save()

    return make_response({"repetition": repetition_schema.dump(repetition).data}, 200)

from datetime import datetime, timedelta
from typing import Optional, Tuple, Iterable

from flask import Blueprint, Response, make_response, request
from sqlalchemy import asc, desc

from goforbroca.api.flashcard import flashcard_schema
from goforbroca.extensions import db, ma
from goforbroca.models.deck import UserDeck
from goforbroca.models.flashcard import Flashcard
from goforbroca.models.repetition import Repetition
from goforbroca.models.user import User
from goforbroca.util.auth import wrap_authenticated_user
from goforbroca.util.sm2 import scores_to_sm2

min_learned_score = 0.95
minutes_in_a_day = 24 * 60
max_refresh_at_offset = timedelta(minutes=5)

repetition_blueprint = Blueprint('repetition', __name__, url_prefix='/api/repetitions')


class RepetitionSchema(ma.ModelSchema):

    user_deck_id = ma.Int(dump_only=True)
    flashcard_id = ma.Int(dump_only=True)

    class Meta:
        model = Repetition
        sqla_session = db.session


repetition_schema = RepetitionSchema()


@repetition_blueprint.route('/', methods=['POST'])
@wrap_authenticated_user
def create_repetition(user: User) -> Response:
    user_deck_id = request.json.get('user_deck_id')
    user_deck_ids = {user_deck.id for user_deck in UserDeck.query.filter_by(user_id=user.id)}

    if user_deck_id is not None:
        if user_deck_id not in user_deck_ids:
            return make_response({"msg": "invalid user_deck_id"}, 400)

        user_deck_ids = {user_deck_id}

    repetition, flashcard = _get_or_create_repetition_and_flashcard(user_deck_ids)
    if repetition is None or flashcard is None:
        return make_response({"msg": "no flashcards to review (try forking a standard deck to get started)"}, 200)

    response = {
        "repetition": repetition_schema.dump(repetition).data,
        "flashcard": flashcard_schema.dump(flashcard).data,
    }
    return make_response(response, 200)


def _get_or_create_repetition_and_flashcard(user_deck_ids: Iterable[int]) -> Optional[Tuple[Repetition, Flashcard]]:

    active_repetition = (Repetition.query
                         .filter(Repetition.user_deck_id.in_(user_deck_ids))
                         .filter(Repetition.active.is_(True))
                         .scalar())
    if active_repetition is not None:
        repetition = active_repetition
        flashcard = Flashcard.query.get(repetition.flashcard_id)
        return repetition, flashcard

    triage_flashcard = (Flashcard.query
                        .filter(Flashcard.user_deck_id.in_(user_deck_ids))
                        .order_by(asc(Flashcard.refresh_at))
                        .limit(1).scalar())

    max_refresh_at = datetime.utcnow() + max_refresh_at_offset
    if not (triage_flashcard < max_refresh_at):
        return None

    flashcard = triage_flashcard
    previous = (Repetition.query
                .filter_by(flashcard_id=flashcard.id)
                .order_by(desc(Repetition.iteration))
                .limit(1).scalar())
    if previous is None:
        repetition = Repetition.create(
            user_id=flashcard.user_id,
            user_deck_id=flashcard.user_deck_id,
            flashcard_id=flashcard.id,
            iteration=1,
            active=True,
            score=None,
        )
    else:
        if previous.active:
            repetition = previous
        else:
            repetition = Repetition.create(
                user_id=flashcard.user_id,
                user_deck_id=flashcard.user_deck_id,
                flashcard_id=flashcard.id,
                iteration=previous.iteration + 1,
                active=True,
                score=None,
            )

    return repetition, flashcard


@repetition_blueprint.route('/<repetition_id>', methods=['POST'])
@wrap_authenticated_user
def submit_repetition_answer(user: User, repetition_id: int) -> Response:
    score = request.json['score']

    repetition = Repetition.query.filter_by(id=repetition_id, user_id=user.id, active=True).scalar()
    if not repetition:
        return make_response({"msg": "repetition not found"}, 404)

    previous = (Repetition.query
                .filter_by(flashcard_id=repetition.flashcard_id, active=False)
                .order_by(asc(Flashcard.completed_at)))

    scores = [r.score for r in previous] + [score]
    refresh_days_offset = scores_to_sm2(scores)
    refresh_minutes_offset = refresh_days_offset * minutes_in_a_day
    refresh_datetime_delta = timedelta(minutes=refresh_minutes_offset)

    flashcard = Flashcard.query.get(repetition.flashcard_id)
    flashcard.refresh_at = datetime.utcnow() + refresh_datetime_delta
    flashcard.save()

    repetition.active = False
    repetition.score = score
    repetition.completed_at = datetime.utcnow()
    repetition.save()

    return make_response({"repetition": repetition_schema.dump(repetition).data}, 200)

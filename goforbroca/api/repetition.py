from datetime import datetime

from flask import Blueprint, Response, make_response, request
from sqlalchemy import asc, or_

from goforbroca.api.flashcard import flashcard_schema
from goforbroca.extensions import db, ma
from goforbroca.models.deck import UserDeck
from goforbroca.models.flashcard import Flashcard
from goforbroca.models.repetition import Repetition
from goforbroca.models.user import User
from goforbroca.util.auth import wrap_authenticated_user

min_learned_score = 0.95

repetition_blueprint = Blueprint('repetition', __name__, url_prefix='/api/repetitions')


class RepetitionSchema(ma.ModelSchema):

    user_deck_id = ma.Int(dump_only=True)
    flashcard_id = ma.Int(dump_only=True)

    class Meta:
        model = Repetition
        sqla_session = db.session


repetition_schema = RepetitionSchema()


# TODO: don't always get the highest ranking card, incorporate last viewed time, progress, etc
@repetition_blueprint.route('/', methods=['POST'])
@wrap_authenticated_user
def create_repetition(user: User) -> Response:
    user_deck_id = request.json.get('user_deck_id')
    user_deck_ids = {user_deck.id for user_deck in UserDeck.query.filter_by(user_id=user.id)}

    if user_deck_id is not None:
        if user_deck_id not in user_deck_ids:
            return make_response({"msg": "invalid user_deck_id"}, 400)

        user_deck_ids = {user_deck_id}

    flashcard = (Flashcard.query
                 .filter(Flashcard.user_deck_id.in_(user_deck_ids))
                 .filter(or_(Flashcard.progress < min_learned_score, Flashcard.progress.is_(None)))
                 .order_by(asc(Flashcard.rank))
                 .limit(1).scalar())

    if not flashcard:
        return make_response({"msg": "no flashcards to review (try forking a standard deck to get started)"}, 200)

    previous = Repetition.query.filter_by(user_id=user.id, flashcard_id=flashcard.id).all()
    if previous:
        if any(repetition.active for repetition in previous):
            repetition = next(r for r in previous if r.active)
        else:
            latest = max(previous, key=lambda r: r.iteration)
            repetition = Repetition.create(
                user_id=user.id,
                user_deck_id=flashcard.user_deck_id,
                flashcard_id=flashcard.id,
                iteration=latest.iteration + 1,
                active=True,
                score=None
            )
    else:
        repetition = Repetition.create(
            user_id=user.id,
            user_deck_id=flashcard.user_deck_id,
            flashcard_id=flashcard.id,
            iteration=1,
            active=True,
            score=None,
        )

    response = {
        "repetition": repetition_schema.dump(repetition).data,
        "flashcard": flashcard_schema.dump(flashcard).data,
    }
    return make_response(response, 200)


@repetition_blueprint.route('/<repetition_id>', methods=['POST'])
@wrap_authenticated_user
def submit_repetition_answer(user: User, repetition_id: int) -> Response:
    score = request.json['score']

    repetition = Repetition.query.filter_by(id=repetition_id, user_id=user.id, active=True).scalar()
    if not repetition:
        return make_response({"msg": "repetition not found"}, 404)

    repetition.active = False
    repetition.score = score
    repetition.completed_at = datetime.utcnow()
    repetition.save()

    # TODO: update progress based on sm2

    return make_response({"repetition": repetition_schema.dump(repetition).data}, 200)

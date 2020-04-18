import random
from typing import Iterable, Optional

from flask import Blueprint, Response, make_response, request
from sqlalchemy import func

from goforbroca.extensions import ma, db
from goforbroca.models.deck import UserDeck, default_standard_deck_max_rank
from goforbroca.models.flashcard import Flashcard
from goforbroca.models.user import User
from goforbroca.util.auth import wrap_authenticated_user
from goforbroca.util.pagination import paginate
from goforbroca.util.rest import get_unique_query_parameters

flashcard_blueprint = Blueprint('flashcards', __name__, url_prefix='/api/flashcards')

list_cards_parameter_to_update_func = {
    'standard_deck_id': lambda query, value: query.filter_by(standard_deck_id=value),
    'user_deck_id': lambda query, value: query.filter_by(user_deck_id=value),
    'min_progress': lambda query, value: query.filter(Flashcard.progress >= value),
    'max_progress': lambda query, value: query.filter(value >= Flashcard.progress),
}

update_card_parameter_to_update_func = {
    'front': lambda flashcard, value: setattr(flashcard, 'front', value),
    'back': lambda flashcard, value: setattr(flashcard, 'back', value),
    'rank': lambda flashcard, value: setattr(flashcard, 'rank', value),
    'progress': lambda flashcard, value: setattr(flashcard, 'progress', value),
}


class FlashcardSchema(ma.ModelSchema):

    standard_deck_id = ma.Int(dump_only=True)
    user_deck_id = ma.Int(dump_only=True)

    class Meta:
        model = Flashcard
        sqla_session = db.session


flashcard_schema = FlashcardSchema()
flashcards_schema = FlashcardSchema(many=True)


@flashcard_blueprint.route('/', methods=['GET'])
@wrap_authenticated_user
def list_cards(user: User) -> Response:
    query_parameters = get_unique_query_parameters()
    page_number = query_parameters.pop('page_number', None)
    page_size = query_parameters.pop('page_size', None)

    query = Flashcard.query.filter_by(user_id=user.id)
    for key, value in query_parameters.items():
        update_func = list_cards_parameter_to_update_func[key]
        query = update_func(query, value)

    response = paginate('flashcards', query, flashcards_schema, page_number, page_size)
    return make_response(response, 200)


@flashcard_blueprint.route('/', methods=['POST'])
@wrap_authenticated_user
def create_card(user: User) -> Response:
    user_deck_id = request.json.get('user_deck_id')
    front = request.json['front']
    back = request.json.get('back')
    rank = request.json.get('rank')
    progress = request.json.get('progress')

    if user_deck_id is not None:
        user_deck = UserDeck.query.filter_by(user_id=user.id, id=user_deck_id).scalar()
        if not user_deck:
            return make_response({'msg': 'user_deck not found'}, 404)

    # TODO: allow back to be optional and translate based on language parameter
    if back is None:
        pass

    # TODO: add sound to cards
    # TODO: handle google TTS credentials file in heroku

    flashcard = Flashcard.create(
        user_deck_id=user_deck_id,
        user_id=user.id,
        front=front,
        back=back,
        rank=rank,
        audio_url=None,
        progress=progress,
    )
    return make_response({'flashcard': flashcard_schema.dump(flashcard).data}, 200)


@flashcard_blueprint.route('/<flashcard_id>', methods=['PUT'])
@wrap_authenticated_user
def update_card(user: User, flashcard_id: int):
    flashcard = Flashcard.query.filter_by(user_id=user.id, id=flashcard_id).scalar()
    if not flashcard:
        return make_response({'msg': 'flashcard not found'}, 404)

    for key, value in request.json.items():
        update_func = update_card_parameter_to_update_func[key]
        update_func(flashcard, value)

    flashcard.save()
    return make_response({'flashcard': flashcard_schema.dump(flashcard).data}, 200)


@flashcard_blueprint.route('/<flashcard_id>', methods=['DELETE'])
@wrap_authenticated_user
def delete_card(user: User, flashcard_id: int):
    flashcard = Flashcard.query.filter_by(user_id=user.id, id=flashcard_id).scalar()
    if not flashcard:
        return make_response({"msg": "flashcard not found"}, 404)

    flashcard.delete()
    return make_response({"flashcard": flashcard_schema.dump(flashcard).data}, 200)


@flashcard_blueprint.route('/view', methods=['POST'])
@wrap_authenticated_user
def view_new_card(user: User) -> Response:
    forked_user_deck_id = request.json.get('user_deck_id')
    forked_user_decks = {user_deck for user_deck in UserDeck.query.filter_by(user_id=user.id, active=True)
                         if user_deck.standard_deck_id is not None}
    if forked_user_deck_id is not None:
        if forked_user_deck_id not in {forked_user_decks}:
            return make_response({"msg": "invalid user_deck_id"}, 400)

        forked_user_deck = UserDeck.query.get(id=forked_user_deck_id)
        forked_user_decks = {forked_user_deck}

    flashcard = _create_next_flashcard(forked_user_decks)
    if flashcard is None:
        return make_response({"msg": "no remaining flashcards to learn"}, 200)

    return make_response({"flashcard": flashcard_schema.dump(flashcard).data}, 200)


def _create_next_flashcard(forked_user_decks: Iterable[UserDeck]) -> Optional[Flashcard]:
    forked_user_deck_ids = {deck.id for deck in forked_user_decks}
    max_rank_per_forked_deck = (db.session.query(Flashcard.user_deck_id, func.max(Flashcard.rank))
                                .filter(Flashcard.user_deck_id.in_(forked_user_deck_ids))
                                .group_by(Flashcard.user_deck_id)).all()
    unstarted_deck_ids = forked_user_deck_ids - {deck_id for deck_id, max_rank in max_rank_per_forked_deck}
    if unstarted_deck_ids:
        user_deck_id = random.choice(tuple(unstarted_deck_ids))
        user_deck = UserDeck.query.get(user_deck_id)
        rank = 1
    else:
        deck_id_and_rank = min(max_rank_per_forked_deck, key=lambda deck_id_and_max_rank: deck_id_and_max_rank[1])
        user_deck_id, max_rank = deck_id_and_rank
        if max_rank == default_standard_deck_max_rank:
            return None

        user_deck = UserDeck.query.get(user_deck_id)
        min_rank_flashcard = Flashcard.query.filter_by(user_deck_id=user_deck_id, rank=max_rank).scalar()
        rank = min_rank_flashcard.rank + 1

    standard_deck_id = user_deck.standard_deck_id
    original = Flashcard.query.filter_by(standard_deck_id=standard_deck_id, rank=rank).scalar()
    if not original:
        return None

    clone = Flashcard.create(
        language_id=original.language_id,
        standard_deck_id=None,
        user_deck_id=user_deck.id,
        user_id=user_deck.user_id,
        front=original.front,
        back=original.back,
        rank=original.rank,
        audio_url=original.audio_url,
    )
    return clone

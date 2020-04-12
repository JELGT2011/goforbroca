from flask import Blueprint, Response, make_response, request
from sqlalchemy import asc, or_

from goforbroca.extensions import ma, db
from goforbroca.models.deck import UserDeck
from goforbroca.models.flashcard import Flashcard
from goforbroca.models.user import User
from goforbroca.util.auth import wrap_authenticated_user
from goforbroca.util.pagination import paginate
from goforbroca.util.rest import get_unique_query_parameters

flashcard_blueprint = Blueprint('flashcards', __name__, url_prefix='/api/flashcards')

list_cards_parameter_to_update_func = {
    'standard_deck_id': lambda query, value: query.filter_by(standard_deck_id=value),
    'user_deck_id': lambda query, value: query.filter_by(user_deck_id=value),
    'viewed': lambda query, value: query.filter_by(viewed=value),
    'min_progress': lambda query, value: query.filter(Flashcard.progress >= value),
    'max_progress': lambda query, value: query.filter(value >= Flashcard.progress),
}

update_card_parameter_to_update_func = {
    'front': lambda flashcard, value: setattr(flashcard, 'front', value),
    'back': lambda flashcard, value: setattr(flashcard, 'back', value),
    'rank': lambda flashcard, value: setattr(flashcard, 'rank', value),
    'viewed': lambda flashcard, value: setattr(flashcard, 'viewed', value),
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
    viewed = request.json.get('viewed', True)
    progress = request.json.get('progress')

    if user_deck_id is not None:
        user_deck = UserDeck.query.filter_by(user_id=user.id, id=user_deck_id).scalar()
        if not user_deck:
            return make_response({'msg': 'user_deck not found'}, 404)

    # TODO: allow back to be optional and translate based on language parameter

    flashcard = Flashcard.create(
        user_deck_id=user_deck_id,
        user_id=user.id,
        front=front,
        back=back,
        rank=rank,
        viewed=viewed,
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
    user_deck_id = request.json.get('user_deck_id')
    user_deck_ids = {user_deck.id for user_deck in UserDeck.query.filter_by(user_id=user.id, active=True)}
    if user_deck_id:
        if user_deck_id not in user_deck_ids:
            return make_response({"msg": "invalid user_deck_id"}, 400)

        flashcard = (Flashcard.query
                     .filter(Flashcard.user_deck_id == user_deck_id)
                     .filter(Flashcard.viewed.is_(False))
                     .order_by(asc(Flashcard.rank))
                     .limit(1)
                     .scalar())
    else:
        flashcard = (Flashcard.query
                     .filter(Flashcard.user_deck_id.in_(user_deck_ids))
                     .filter(Flashcard.viewed.is_(False))
                     .order_by(asc(Flashcard.rank))
                     .limit(1)
                     .scalar())

    if not flashcard:
        return make_response({"msg": "no remaining flashcards to learn"}, 200)

    flashcard.viewed = True
    flashcard.save()

    return make_response({"flashcard": flashcard_schema.dump(flashcard).data}, 200)

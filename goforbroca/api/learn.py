from flask import Blueprint, Response, make_response, request

from goforbroca.api.auth import wrap_authenticated_user
from goforbroca.models.deck import UserDeck, StandardDeck
from goforbroca.models.user import User

learn_blueprint = Blueprint('learn', __name__, url_prefix='/api/learn')


@learn_blueprint.route('/', methods=['POST'])
@wrap_authenticated_user
def get_new_card(user: User) -> Response:
    deck_id = request.json.get('deck_id')
    if deck_id is None:
        user_decks = UserDeck.query.filter_by(user_id=user.id)
        standard_decks = StandardDeck.query.filter_by(id__in=[user_deck.standard_deck_id for user_deck in user_decks])
        deck_id = 1  # TODO

    pass
    return make_response(200)

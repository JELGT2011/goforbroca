from flask import Blueprint, Response, make_response, request

from goforbroca.api.auth import wrap_authenticated_user
from goforbroca.extensions import db, ma
from goforbroca.models.deck import StandardDeck, UserDeck
from goforbroca.models.user import User

deck_blueprint = Blueprint('deck', __name__, url_prefix='/api/decks')


class StandardDeckSchema(ma.ModelSchema):

    class Meta:
        model = StandardDeck
        sqla_session = db.session


standard_deck_schema = StandardDeckSchema()
standard_decks_schema = StandardDeckSchema(many=True)


class UserDeckSchema(ma.ModelSchema):

    standard_deck_id = ma.Int(dump_only=True)

    class Meta:
        model = UserDeck
        sqla_session = db.session


user_deck_schema = UserDeckSchema()
user_decks_schema = UserDeckSchema(many=True)


@deck_blueprint.route('/standard', methods=['GET'])
@wrap_authenticated_user
def get_standard_decks(user: User) -> Response:
    decks = StandardDeck.query.all()
    return make_response({'decks': standard_decks_schema.dump(decks).data}, 200)


@deck_blueprint.route('/user', methods=['GET'])
@wrap_authenticated_user
def get_user_decks(user: User) -> Response:
    decks = UserDeck.query.filter_by(user_id=user.id)
    return make_response({'decks': user_decks_schema.dump(decks).data}, 200)


@deck_blueprint.route('/standard/fork', methods=['POST'])
@wrap_authenticated_user
def fork_standard_deck(user: User) -> Response:
    standard_deck_id = request.json['standard_deck_id']
    standard_deck = StandardDeck.query.get(standard_deck_id)
    user_deck = UserDeck.query.filter_by(user_id=user.id, standard_deck_id=standard_deck.id).scalar()
    if user_deck:
        return make_response({'msg': 'deck has already been forked'}, 400)

    user_deck = UserDeck.create(
        name=standard_deck.name,
        standard_deck_id=standard_deck.id,
        user_id=user.id,
        active=True,
    )
    return make_response({'decks': user_deck_schema.dump(user_deck).data}, 200)


@deck_blueprint.route('/user/', methods=['POST'])
@wrap_authenticated_user
def create_user_deck(user: User) -> Response:
    name = request.json['name']
    user_deck = UserDeck.create(name=name, standard_deck_id=None, user_id=user.id, active=True)
    return make_response({'deck': user_deck_schema.dump(user_deck).data}, 200)

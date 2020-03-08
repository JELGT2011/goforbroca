from flask import Blueprint, Response, make_response, request

from goforbroca.api.auth import wrap_authenticated_user
from goforbroca.extensions import db, ma
from goforbroca.models.deck import StandardDeck, UserDeck
from goforbroca.models.flashcard import Flashcard
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


@deck_blueprint.route('/standard/<standard_deck_id>/fork', methods=['POST'])
@wrap_authenticated_user
def fork_standard_deck(user: User, standard_deck_id: int) -> Response:
    standard_deck = StandardDeck.query.get(standard_deck_id)
    user_deck = UserDeck.query.filter_by(user_id=user.id, standard_deck_id=standard_deck.id).scalar()
    if user_deck is not None:
        return make_response({'msg': 'deck has already been forked'}, 400)

    user_deck = UserDeck.create(
        name=standard_deck.name,
        standard_deck_id=standard_deck.id,
        user_id=user.id,
        active=True,
    )

    standard_deck_flashcards = Flashcard.query.filter_by(standard_deck_id=standard_deck_id)
    for flashcard in standard_deck_flashcards:
        db.session.add(
            Flashcard(
                standard_deck_id=None,
                user_deck_id=user_deck.id,
                front=flashcard.front,
                back=flashcard.back,
                rank=flashcard.rank,
                max_score=0,
            )
        )
    db.session.commit()

    return make_response({'deck': user_deck_schema.dump(user_deck).data}, 200)


@deck_blueprint.route('/user', methods=['POST'])
@wrap_authenticated_user
def create_user_deck(user: User) -> Response:
    name = request.json['name']
    active = request.json.get('active', True)
    user_deck = UserDeck.create(name=name, standard_deck_id=None, user_id=user.id, active=active)
    return make_response({'deck': user_deck_schema.dump(user_deck).data}, 200)


@deck_blueprint.route('/user/<user_deck_id>', methods=['PUT'])
@wrap_authenticated_user
def update_user_deck(user: User, user_deck_id: int) -> Response:
    user_deck = UserDeck.query.filter_by(id=user_deck_id, user_id=user.id).scalar()
    if not user_deck:
        return make_response({'msg': 'user deck not found'}, 404)

    user_deck.name = request.json.get('name', user_deck.name)
    user_deck.active = request.json.get('active', user_deck.active)
    user_deck.save()

    return make_response({'deck': user_deck_schema.dump(user_deck).data}, 200)


@deck_blueprint.route('/user/<user_deck_id>', methods=['DELETE'])
@wrap_authenticated_user
def delete_user_deck(user: User, user_deck_id: int) -> Response:
    user_deck = UserDeck.query.filter_by(id=user_deck_id, user_id=user.id).scalar()
    if not user_deck:
        return make_response({'msg': 'user deck not found'}, 404)

    Flashcard.query.filter_by(user_deck_id=user_deck_id).delete()
    db.session.delete(user_deck)
    db.session.commit()

    return make_response({'deck': user_deck_schema.dump(user_deck).data}, 200)

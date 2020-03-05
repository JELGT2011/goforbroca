from flask import Blueprint, Response, make_response, request
from sqlalchemy import asc, or_

from goforbroca.api.auth import wrap_authenticated_user
from goforbroca.extensions import ma, db
from goforbroca.models.deck import UserDeck
from goforbroca.models.flashcard import Flashcard
from goforbroca.models.user import User

min_learned_score = 0.9

learn_blueprint = Blueprint('learn', __name__, url_prefix='/api/learn')


class FlashcardSchema(ma.ModelSchema):

    class Meta:
        model = Flashcard
        sqla_session = db.session


flashcard_schema = FlashcardSchema()


@learn_blueprint.route('/', methods=['POST'])
@wrap_authenticated_user
def get_new_card(user: User) -> Response:
    user_deck_ids = {user_deck.id for user_deck in UserDeck.query.filter_by(user_id=user.id)}

    user_deck_id = request.json.get('user_deck_id')
    if user_deck_id:
        if user_deck_id not in user_deck_ids:
            return make_response({"msg": "invalid user_deck_id"}, 400)

        flashcard = (Flashcard.query
                     .filter(Flashcard.user_deck_id == user_deck_id)
                     .filter(or_(Flashcard.max_score < min_learned_score, Flashcard.max_score.is_(None)))
                     .order_by(asc(Flashcard.rank))
                     .limit(1)
                     .scalar())
    else:
        flashcard = (Flashcard.query
                     .filter(Flashcard.user_deck_id.in_(user_deck_ids))
                     .filter(or_(Flashcard.max_score < min_learned_score, Flashcard.max_score.is_(None)))
                     .order_by(asc(Flashcard.rank))
                     .limit(1)
                     .scalar())

    if not flashcard:
        return make_response({"msg": "no remaining flashcards to learn"}, 200)

    return make_response({"flashcard": flashcard_schema.dump(flashcard).data}, 200)

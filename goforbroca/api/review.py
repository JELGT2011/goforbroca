from flask import Blueprint, Response, make_response

from goforbroca.api.auth import wrap_authenticated_user
from goforbroca.models.user import User

review_blueprint = Blueprint('review', __name__, url_prefix='/api/review')


@review_blueprint.route('/', methods=['GET'])
@wrap_authenticated_user
def get_review_card(user: User) -> Response:
    pass
    return make_response(200)

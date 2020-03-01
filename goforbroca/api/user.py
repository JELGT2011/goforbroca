from flask import Response, Blueprint, request, make_response

from goforbroca.api.auth import wrap_google_auth_user
from goforbroca.models.user import User

user_blueprint = Blueprint('user', __name__, url_prefix='/api/users')


@user_blueprint.route('/', methods=['GET'])
@wrap_google_auth_user
def get(google_id) -> Response:
    user = User.query.filter_by(google_id=google_id).first()
    if user is None:
        return make_response({'msg': 'user does not exist', 'user': {'google_id': google_id}}, 404)

    return make_response({'msg': 'ok', 'user': user.to_json()}, 200)


@user_blueprint.route('/', methods=['POST'])
@wrap_google_auth_user
def post(google_id) -> Response:
    user = User.query.filter_by(google_id=google_id).first()
    if user is not None:
        return make_response({'msg': 'user already exists'}, 400)

    user = User.create(google_id=google_id)
    return make_response({'msg': 'user created', 'user': user.to_json()}, 201)


@user_blueprint.route('/', methods=['PUT'])
@wrap_google_auth_user
def put(google_id) -> Response:
    user = User.query.filter_by(google_id=google_id).first()
    if user is None:
        return make_response({'msg': 'user does not exist', 'user': {'google_id': google_id}}, 404)

    raise NotImplementedError()
    # return make_response({'msg': 'user successfully updated', 'user': user.to_json()}, 200)

from flask import Response, Blueprint, make_response

from goforbroca.api.auth import wrap_authenticated_user, wrap_google_user
from goforbroca.extensions import db, ma
from goforbroca.models.user import User

user_blueprint = Blueprint('user', __name__, url_prefix='/api/users')


class UserSchema(ma.ModelSchema):

    class Meta:
        model = User
        sqla_session = db.session


user_schema = UserSchema()


@user_blueprint.route('/', methods=['POST'])
@wrap_google_user
def post(google_id: str) -> Response:
    user = User.query.filter_by(google_id=google_id).scalar()
    if user is not None:
        return make_response({'msg': 'user already exists'}, 400)

    user = User.create(google_id=google_id)
    return make_response({'user': user_schema.dump(user).data}, 201)


@user_blueprint.route('/', methods=['GET'])
@wrap_authenticated_user
def get(user: User) -> Response:
    return make_response({'user': user_schema.dump(user).data}, 200)


@user_blueprint.route('/', methods=['PUT'])
@wrap_authenticated_user
def put(user: User) -> Response:
    raise NotImplementedError()
    # return make_response({'user': user_schema.dump(user).data}, 200)

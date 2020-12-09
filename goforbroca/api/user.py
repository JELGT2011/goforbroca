from flask import Response, Blueprint, make_response, request

from goforbroca.api.deck import user_deck_schema
from goforbroca.extensions import db, ma
from goforbroca.models.deck import UserDeck
from goforbroca.models.user import User
from goforbroca.util.auth import wrap_authenticated_user, wrap_google_user

user_blueprint = Blueprint('user', __name__, url_prefix='/api/users')


class UserSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = User
        sqla_session = db.session


user_schema = UserSchema()


@user_blueprint.route('/', methods=['POST'])
@wrap_google_user
def post(google_id: str) -> Response:
    email_address = request.json['email']

    user = User.query.filter_by(google_id=google_id).scalar()
    if user is not None:
        return make_response({'msg': 'user already exists'}, 400)

    user = User.create(email_address=email_address, google_id=google_id,sms_enabled=False)
    user_deck = UserDeck.create_default_deck(user.id)
    return make_response({'user': user_schema.dump(user).data, 'user_deck': user_deck_schema.dump(user_deck).data}, 200)


@user_blueprint.route('/', methods=['GET'])
@wrap_authenticated_user
def get(user: User) -> Response:
    return make_response({'user': user_schema.dump(user).data}, 200)


@user_blueprint.route('/', methods=['PUT'])
@wrap_authenticated_user
def put(user: User) -> Response:
    sms_enabled = request.json.get('sms_enabled')
    phone_number = request.json.get('phone_number')

    user = User.query.filter_by(id=user.id).scalar()

    if sms_enabled is not None:    
        user.sms_enabled = sms_enabled
    if phone_number is not None:
        user.phone_number = phone_number
    
    user.save()

    return make_response({'user': user_schema.dump(user).data}, 200)
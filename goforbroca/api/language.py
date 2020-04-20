from flask import Blueprint, Response, make_response

from goforbroca.extensions import db, ma
from goforbroca.models.language import Language
from goforbroca.models.user import User
from goforbroca.util.auth import wrap_authenticated_user

language_blueprint = Blueprint('languages', __name__, url_prefix='/api/languages')


class LanguageSchema(ma.ModelSchema):

    class Meta:
        model = Language
        sqla_session = db.session


language_schema = LanguageSchema()
languages_schema = LanguageSchema(many=True)


@language_blueprint.route('/', methods=['GET'])
@wrap_authenticated_user
def list_languages(user: User) -> Response:
    languages = Language.query.all()
    return make_response({'languages': languages_schema.dump(languages).data}, 200)

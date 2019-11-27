from flask import Blueprint
from flask_restful import Api

from goforbroca.api.resources.message import MessageResource
from goforbroca.api.resources.privacy import PrivacyResource
from goforbroca.api.resources.root import RootResource

blueprint = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(blueprint)


api.add_resource(RootResource, '/')
api.add_resource(PrivacyResource, '/privacy')
api.add_resource(MessageResource, '/message')

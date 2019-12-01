from flask import Blueprint
from flask_restful import Api

from goforbroca.api.resources.message import MessageResource

blueprint = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(blueprint)


api.add_resource(MessageResource, '/message')

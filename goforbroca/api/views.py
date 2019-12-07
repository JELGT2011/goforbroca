from flask import Blueprint
from flask_restful import Api

from goforbroca.api.resources.sms import SMSResource

blueprint = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(blueprint)


api.add_resource(SMSResource, '/sms')

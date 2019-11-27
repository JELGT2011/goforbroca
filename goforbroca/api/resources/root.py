from flask import Response
from flask_restful import Resource


class RootResource(Resource):

    ROOT_MESSAGE = "Hello there, I'm a facebook messenger bot."

    @classmethod
    def get(cls) -> Response:
        return Response(cls.ROOT_MESSAGE)

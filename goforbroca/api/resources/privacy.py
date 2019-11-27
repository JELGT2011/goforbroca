from flask import Response
from flask_restful import Resource


class PrivacyResource(Resource):

    PRIVACY_POLICY = """
    This facebook messenger bot's only purpose is to `the`.
    That's all. We don't use it in any other way. As we should.
    `The` is love, `the` is life.
    """

    @classmethod
    def get(cls) -> Response:
        return Response(cls.PRIVACY_POLICY)

from flask import Flask
from flask_restful import Api

from .resource.account import Account
from .resource.common import Random


def create_app():

    app = Flask(__name__)
    api = Api(app)
    api.add_resource(Account, '/account/<string:website>')
    api.add_resource(Random, '/cookies/<string:website>/random')

    return app

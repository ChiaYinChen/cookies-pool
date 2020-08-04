from flask import Flask
from flask_restful import Api

from .resource.account import Account
from .resource.cookies import Cookies


def create_app():

    app = Flask(__name__)
    api = Api(app)
    api.add_resource(Account, '/account/<string:website>/')
    api.add_resource(Cookies, '/cookies/<string:website>/<string:_type>/')

    return app

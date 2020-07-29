"""API for account."""
from flask import request
from flask_restful import Resource

from cookies_pool.db.clients import RedisClient


class Account(Resource):
    """Account."""

    def post(self, website):
        """Add account/password."""
        data = request.get_json()
        account = data.get('account')
        password = data.get('password')
        params = {
            'website': website,
            'account': account,
            'password': password,
        }
        accounts_db = RedisClient(type_='accounts', website=website)
        if accounts_db.get(account):
            return {'message': 'Account is exist!'}
        if accounts_db.set(account=account, value=password):
            return {
                'message': 'Add account success',
                'params': params
            }, 201

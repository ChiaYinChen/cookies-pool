"""API for account."""
from flask_restful import Resource, reqparse

from cookies_pool.db.clients import RedisClient


class Account(Resource):
    """Account."""

    def __init__(self, *args, **kwargs):
        """Init."""
        super().__init__(*args, **kwargs)
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(
            'account', type=str, required=True, help='required account'
        )
        self.parser.add_argument(
            'password', type=str, required=True, help='required password'
        )

    def post(self, website: str):
        """Add account/password.

        Args:
            website (str): website name, e.g. 'fb', 'ig'
        """
        data = self.parser.parse_args()
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

    def put(self, website: str):
        """Update account.

        Args:
            website (str): website name, e.g. 'fb', 'ig'
        """
        data = self.parser.parse_args()
        account = data.get('account')
        password = data.get('password')
        params = {
            'website': website,
            'account': account,
            'password': password,
        }
        accounts_db = RedisClient(type_='accounts', website=website)
        if accounts_db.get(account):
            accounts_db.set(account=account, value=password)
            return {
                'message': 'Update account success',
                'params': params
            }
        else:
            return {'message': 'Account not found!'}, 404

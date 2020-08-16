"""API for account."""
from flask_restful import Resource, reqparse

from cookies_pool.db.clients import RedisClient


class Account(Resource):
    """Account."""

    def __init__(self, *args, **kwargs):
        """Initialize."""
        super().__init__(*args, **kwargs)
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(
            'account', type=str, required=True, help='required account'
        )
        self.parser.add_argument(
            'password', type=str, required=True, help='required password'
        )

    def account_input(self, data: reqparse.Namespace) -> dict:
        """Request parameters.

        Args:
            data (reqparse.Namespace): reqparse object

        Returns:
            dict: request parameters
        """
        account = data.get('account')
        password = data.get('password')
        return {
            'account': account,
            'password': password,
        }

    def post(self, website: str):
        """Add account/password.

        Args:
            website (str): website name, e.g. 'fb', 'ig'
        """
        params = self.account_input(data=self.parser.parse_args())
        accounts_db = RedisClient(type_='accounts', website=website)
        if accounts_db.get(params.get('account')):
            return {'message': 'Account is exist!'}
        if accounts_db.set(
            account=params.get('account'), value=params.get('password')
        ):
            return {
                'message': 'Add account success',
                'website': website,
                'params': params
            }, 201

    def put(self, website: str):
        """Update account.

        Args:
            website (str): website name, e.g. 'fb', 'ig'
        """
        params = self.account_input(data=self.parser.parse_args())
        accounts_db = RedisClient(type_='accounts', website=website)
        if accounts_db.get(params.get('account')):
            accounts_db.set(
                account=params.get('account'), value=params.get('password')
            )
            return {
                'message': 'Update account success',
                'website': website,
                'params': params
            }
        else:
            return {'message': 'Account not found!'}, 404

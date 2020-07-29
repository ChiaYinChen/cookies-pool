"""Common API."""
from flask_restful import Resource

from cookies_pool.db.clients import RedisClient


class Random(Resource):
    """Random."""

    def get(self, website):
        """Get a random cookies."""
        cookies_db = RedisClient(type_='cookies', website=website)
        if cookies_db.count():
            return cookies_db.random()
        return {
            'message': f'尚未有可用的 {website} cookies!'
        }, 404

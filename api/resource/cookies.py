"""API for cookies."""
import random

from flask_restful import Resource

from cookies_pool.db.clients import RedisClient


class Cookies(Resource):
    """Cookies."""

    def get(self, website, _type):
        """Get cookies."""
        cookies_db = RedisClient(type_='cookies', website=website)
        if cookies_db.count():
            if _type == 'all':
                cookies = cookies_db.get_all_cookies()
            elif _type == 'random':
                cookies = random.choice(cookies_db.get_all_cookies())
            else:
                return {'message': 'Invalid route!'}, 404
            return {
                'message': f'Get {website} cookies success',
                'cookies': cookies
            }
        return {'message': f'尚未有可用的 {website} cookies!'}, 404

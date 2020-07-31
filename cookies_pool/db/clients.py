"""Handle database."""
import redis
from typing import List

from ..settings import REDIS_SETTINGS


class RedisClient:
    """Client wrapper for Redis server."""

    def __init__(self, type_: str, website: str, db: int = 0):
        """Build redis connection.

        Args:
            type_ (str):  value type, e.g. 'accounts', 'cookies'
            website (str): website name, e.g. 'fb', 'ig'
            db (int): redis database index
        """
        REDIS_SETTINGS['db'] = db
        self.conn = redis.StrictRedis(**REDIS_SETTINGS)
        self.type_ = type_
        self.website = website

    @property
    def key_for(self) -> str:
        """Creates unique identifiers to be used as hash keys in Redis.

        Returns:
            str: hash key
        """
        return f'{self.type_}:{self.website}'

    def set(self, account: str, value: str) -> int:
        """Add field (account) / value (password or cookies) pairs.

        Args:
            account (str): user account
            value (str): user password or cookies

        Returns:
            int: the number of fields that were added
        """
        return self.conn.hset(self.key_for, account, value)

    def get(self, account: str) -> str:
        """Returns the value (password or cookies) associated with
           field (account) in the hash stored at key.

        Args:
            account (str): user account

        Returns:
            str: the value associated with field
        """
        value = self.conn.hget(self.key_for, account)
        if value:
            return value.decode('utf-8')

    def get_all_accounts(self) -> List[str]:
        """Returns all field names (accounts) in the hash stored at key.

        Returns:
            List[str]: list of accounts
        """
        accounts = self.conn.hkeys(self.key_for)
        return [account.decode('utf-8') for account in accounts]

    def get_all(self) -> dict:
        """Returns all fields (account) and values (password or cookies)
           of the hash stored at key.

        Returns:
            dict: list of accounts and their values
        """
        data = self.conn.hgetall(self.key_for)
        return {key.decode(): val.decode() for key, val in data.items()}

    def delete(self, account: str) -> int:
        """Removes the specified fields (accounts) from the hash stored at key.

        Args:
            account (str): user account

        Returns:
            int: the number of fields to be removed
        """
        return self.conn.hdel(self.key_for, account)

    def get_all_cookies(self) -> List[str]:
        """Returns all values (cookies) in the hash stored at key.

        Returns:
            List[str]: list of cookies
        """
        cookies = self.conn.hvals(self.key_for)
        return [cookie.decode('utf-8') for cookie in cookies]

    def count(self) -> int:
        """Returns the number of fields (accounts) contained
           in the hash stored at key.

        Returns:
            int: number of fields in the hash, or 0 when key does not exist
        """
        return self.conn.hlen(self.key_for)

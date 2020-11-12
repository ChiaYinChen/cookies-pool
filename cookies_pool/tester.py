"""Tester."""
import abc
import json
import logging

import requests

from . import settings
from .db.clients import RedisClient

logger = logging.getLogger(__name__)


class CookiesTester(abc.ABC):
    """Abstract class for Cookies Tester."""

    def __init__(self, website=None, *args, **kwargs):
        """Initialize.

        Args:
            website (str): website name, e.g. 'fb', 'ig'
        """
        self.website = website or 'default'
        self.accounts_db = RedisClient(type_='accounts', website=self.website)
        self.cookies_db = RedisClient(type_='cookies', website=self.website)

    @abc.abstractmethod
    def test(self, account, cookies):
        """Implement this method for test cookies."""
        pass

    def run(self):
        """Execute the following steps:

        1. Get all account's cookies.
        2. Check if cookies is still valid.
        """
        cookies_groups = self.cookies_db.get_all()
        if cookies_groups:
            for account, cookies in cookies_groups.items():
                self.test(account, cookies)
        else:
            logger.info(f'資料庫尚未有 {self.website} cookies！')


class FBCookiesTester(CookiesTester):
    """Cookies tester for facebook."""

    def __init__(self, website=None, *args, **kwargs):
        """Initialize."""
        super().__init__(website, *args, **kwargs)

    def test(self, account: str, cookies: str):
        """Test the facebook cookies.

        Args:
            account (str): user account
            cookies (str): account's cookies
        """
        cookiejar = requests.utils.cookiejar_from_dict(json.loads(cookies))
        response = requests.get(
            url='https://www.facebook.com/',
            cookies=cookiejar,
            headers={
                'user-agent': settings.USER_AGENT,
                'accept': 'text/html'
            },
            allow_redirects=False
        )
        if (
            response.status_code == 200
        ) and (
            'href="/me/"' in response.text
        ):
            logger.info(f'Cookies 有效 ({account})')
        else:
            logger.error(f'<{response.status_code}> Cookies 失效 ({account})')
            self.cookies_db.delete(account)
            logger.info(f'刪除 Cookies ({account})')


class IGCookiesTester(CookiesTester):
    """Cookies tester for Instagram."""

    def __init__(self, website=None, *args, **kwargs):
        """Initialize."""
        super().__init__(website, *args, **kwargs)

    def test(self, account: str, cookies: str):
        """Test the instagram cookies.

        Args:
            account (str): user account
            cookies (str): account's cookies
        """
        cookiejar = requests.utils.cookiejar_from_dict(json.loads(cookies))
        response = requests.get(
            url='https://www.instagram.com/',
            cookies=cookiejar,
            headers={'user-agent': settings.USER_AGENT},
            allow_redirects=False
        )
        if (
            response.status_code == 200
        ) and (
            f'"username":"{account.lower()}"' in response.text
        ):
            logger.info(f'Cookies 有效 ({account})')
        else:
            logger.error(f'<{response.status_code}> Cookies 失效 ({account})')
            self.cookies_db.delete(account)
            logger.info(f'刪除 Cookies ({account})')

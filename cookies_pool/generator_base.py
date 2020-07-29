"""Base class for Cookies Generator."""
import abc
import json
import logging
import os
from distutils.util import strtobool
from typing import List

from selenium import webdriver

from . import settings
from .db.clients import RedisClient

logger = logging.getLogger(__name__)


class CookiesGenerator(abc.ABC):
    """Abstract class for Cookies Generator."""

    def __init__(self, website=None, *args, **kwargs):
        """Initialize.

        Args:
            website (str): website name, e.g. 'fb', 'ig'
        """
        self.website = website or 'default'
        self.accounts_db = RedisClient(type_='accounts', website=self.website)
        self.cookies_db = RedisClient(type_='cookies', website=self.website)

    def __del__(self):
        """End driver."""
        self.close()

    def init_browser(self):
        """Start driver."""
        selenium_hub = os.environ.get('SELENIUM_HUB', 'selenium-hub')
        remote = bool(strtobool(os.environ.get('REMOTE_ENABLEED', 'TRUE')))

        firefox_options = webdriver.FirefoxProfile()
        # disable notification
        firefox_options.set_preference('dom.webnotifications.enabled', False)
        capabilities = webdriver.DesiredCapabilities.FIREFOX
        if remote:
            self.driver = webdriver.Remote(
                command_executor=f'http://{selenium_hub}:4444/wd/hub',
                desired_capabilities=capabilities,
                browser_profile=firefox_options)
        else:
            self.driver = webdriver.Firefox(
                executable_path=settings.DRIVER_PATH,
                firefox_profile=firefox_options
            )
        self.driver.set_window_size(1920, 1080)

    @abc.abstractmethod
    def new_cookies(self, account, password):
        """Implement this method for create cookies."""
        pass

    def process_cookies(self, cookies: List[dict]) -> dict:
        """Process cookies.

        Args:
            cookies (List[dict]): account's cookies

        Returns:
            dict: list of cookies
        """
        return {cookie['name']: cookie['value'] for cookie in cookies}

    def close(self):
        """Closes all browser windows and ends driver's session/process."""
        if getattr(self, 'driver', None):
            self.driver.quit()
            logger.info('quit driver')

    def run(self):
        """Execute the following steps:

        1. Get all accounts stored in redis.
        2. Login into application and generate the cookies.
        3. Save cookies to redis.
        """
        accounts = self.accounts_db.get_all_accounts()
        if accounts:
            self.init_browser()
            for account in accounts:
                password = self.accounts_db.get(account)
                result = self.new_cookies(account, password)
                if result.get('status'):
                    cookies = self.process_cookies(result.get('content'))
                    logger.debug(f'成功取得 Cookies: {cookies}')
                    if self.cookies_db.set(
                        account=account, value=json.dumps(cookies)
                    ):
                        logger.debug('成功儲存 Cookies')
                else:
                    logger.error(f'{result.get("content")}')
        else:
            logger.info(f'資料庫尚未有 {self.website} 帳號密碼！')

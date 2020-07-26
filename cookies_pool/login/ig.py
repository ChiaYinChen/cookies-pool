"""Emulate browser - instagram."""
import logging
import time

from .base import LoginBase

logger = logging.getLogger(__name__)


class IGCookies(LoginBase):
    """Login into instagram and generate the cookies."""

    def login(self):
        """Instagram login."""
        self.driver.delete_all_cookies()
        self.driver.get(self.url)
        time.sleep(5)
        self.driver.find_element_by_css_selector(
            'input[name="username"]').send_keys(self.account)
        self.driver.find_element_by_css_selector(
            'input[name="password"]').send_keys(self.password)
        self.driver.find_element_by_css_selector(
            '[type=submit]').click()
        time.sleep(5)

    @property
    def logged_in(self):
        """Check if a user has logged in."""
        if 'data-testid="user-avatar"' in self.driver.page_source:
            stat = True
        else:
            stat = False
        logger.info(f'logged in: {stat} ({self.account})')
        return stat

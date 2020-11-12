"""Emulate browser - facebook."""
import logging
import time

from .base import LoginBase

logger = logging.getLogger(__name__)


class FBCookies(LoginBase):
    """Login into facebook and generate the cookies."""

    def login(self):
        """Facebook login."""
        self.driver.delete_all_cookies()
        self.driver.get(self.url)
        time.sleep(1)
        self.driver.find_element_by_css_selector(
            '#email').send_keys(self.account)
        self.driver.find_element_by_css_selector(
            '#pass').send_keys(self.password)
        self.driver.find_element_by_css_selector(
            'button[name="login"]').click()
        time.sleep(1)

    @property
    def logged_in(self):
        """Check if a user has logged in."""
        if 'href="/me/"' in self.driver.page_source:
            stat = True
        else:
            stat = False
        logger.info(f'logged in: {stat} ({self.account})')
        return stat

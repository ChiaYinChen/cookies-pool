"""Generator."""
from .generator_base import CookiesGenerator
from .login.fb import FBCookies
from .login.ig import IGCookies


class FBCookiesGenerator(CookiesGenerator):
    """Cookies generator for facebook."""

    def __init__(self, website=None, *args, **kwargs):
        """Initialize."""
        super().__init__(website, *args, **kwargs)

    def new_cookies(self, account: str, password: str) -> FBCookies:
        """Generate the facebook cookies.

        Args:
            account (str): user account
            password (str): user password

        Returns:
            FBCookies: FBCookies object
        """
        return FBCookies(
            website=self.website,
            account=account,
            password=password,
            driver=self.driver
        ).execute()


class IGCookiesGenerator(CookiesGenerator):
    """Cookies generator for Instagram."""

    def __init__(self, website=None, *args, **kwargs):
        """Initialize."""
        super().__init__(website, *args, **kwargs)

    def new_cookies(self, account: str, password: str) -> IGCookies:
        """Generate the instagram cookies.

        Args:
            account (str): user account
            password (str): user password

        Returns:
            IGCookies: IGCookies object
        """
        return IGCookies(
            website=self.website,
            account=account,
            password=password,
            driver=self.driver
        ).execute()

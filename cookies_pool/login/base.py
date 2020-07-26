"""Base class for Login."""
import abc

LOGIN_URL = {
    'fb': 'https://www.facebook.com/',
    'ig': 'https://www.instagram.com/accounts/login/',
}


class LoginBase(abc.ABC):
    """Abstract class for Login."""

    def __init__(self, website: str, account: str, password: str, driver):
        """Initialize.

        Args:
            website (str): website name, e.g. 'fb', 'ig'
            account (str): user account
            password (str): user password
            driver : browser driver
        """
        self.url = LOGIN_URL.get(website)
        self.account = account
        self.password = password
        self.driver = driver

    @abc.abstractmethod
    def login(self):
        """Implement this method for login into application."""
        pass

    @abc.abstractmethod
    def logged_in(self):
        """Implement this method for check user login stat."""
        pass

    def execute(self):
        """Execute main program."""
        self.login()
        if self.logged_in:
            cookies = self.driver.get_cookies()
            return {
                'status': 1,
                'content': cookies
            }
        else:
            return {
                'status': 0,
                'content': 'login failed'
            }

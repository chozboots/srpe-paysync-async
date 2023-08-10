# standard
import logging


logger = logging.getLogger(__name__)

class LoginError(Exception):
    """Exception raised for errors during the login process."""
    def __init__(self, message):
        self.message = message

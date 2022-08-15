class BaseCdrtException(Exception):
    """Custom base class to reprent exceptions in this template.

    Attributes:
        loggable (Exception): the original error to display in logs (may contain sensible informations to hide from user).
        msg (str): a friendly message to display representing the error for the user.
    """

    def __init__(self, loggable: str = "", msg: str = ""):
        self.loggable = loggable
        self.msg = msg


class DecodeTokenError(BaseCdrtException):
    """Custom class to express an exception while token decoding."""

    pass


class ValidateTokenError(BaseCdrtException):
    """Custom class to express an exception while token validation."""

    pass

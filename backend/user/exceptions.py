"""
Defines custom exceptions specific to the User module.
"""
from backend.libs.exceptions import AlreadyExists, NotFound


class UserAlreadyExists(AlreadyExists):
    """
    Raised when attempting to create a user with a username or email
    that is already in use.
    """
    pass


class UserNotFound(NotFound):
    """
    Raised when a user is not found in the database.
    """
    pass
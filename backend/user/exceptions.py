"""Defines custom exceptions specific to the User module.

This module contains custom exception classes that are specific to the
user-related domain of the application. These exceptions inherit from
the more general application-wide exceptions defined in `libs.exceptions`
but provide a more specific context for error handling. Using these
specific exceptions allows for more granular error responses and clearer
separation of concerns in the application's exception handling logic.
"""
from backend.libs.exceptions import AlreadyExists, NotFound, AccessForbidden


class UserAlreadyExists(AlreadyExists):
    """Raised when creating a user that already exists.

    This exception should be triggered when an attempt to create a new user
    fails because another user with the same unique identifier (e.g., username
    or email address) is already present in the database. It inherits from
    the generic `AlreadyExists` exception.
    """
    pass


class UserNotFound(NotFound):
    """Raised when a requested user is not found.

    This exception is intended to be used when a database query or lookup for
    a user by a specific identifier (like user ID or email) fails to return
    a result. It inherits from the generic `NotFound` exception.
    """
    pass


class UserAccessForbidden(AccessForbidden):
    """Raised on unauthorized access to another user's resources.

    This exception is used to handle authorization errors where an authenticated
    user attempts to perform an action (e.g., view, update, or delete) on
    resources that belong to another user, and such an action is not permitted
    by the business logic. It inherits from the generic `AccessForbidden`
    exception.
    """
    pass
"""Defines custom exceptions specific to the Task module.

This module contains custom exception classes for handling errors related to
task operations. These exceptions inherit from the more general, application-wide
exceptions found in `libs.exceptions` to allow for centralized handling of
common error types (like 'Not Found' or 'Forbidden') while still providing
specific, context-rich exceptions for the task domain.
"""
from backend.libs.exceptions import NotFound, AccessForbidden


class TaskNotFound(NotFound):
    """Raised when a specific task is not found in the database.

    This exception should be used when a query for a task by its primary key
    or another unique identifier fails to return a result. It helps distinguish
    between a failure to find a task versus a failure to find another type of
    resource, like a user.
    """
    pass


class TaskAccessForbidden(AccessForbidden):
    """Raised when a user attempts to access a task they do not own.

    This exception is intended for the service layer to signal an authorization
    failure. It should be raised when an authenticated user tries to perform
    an action (such as viewing, updating, or deleting) on a task that is
    owned by a different user.
    """
    pass
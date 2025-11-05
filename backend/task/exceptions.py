"""
Defines custom exceptions specific to the Task module.
"""
from backend.libs.exceptions import NotFound


class TaskNotFound(NotFound):
    """
    Raised when a specific task is not found in the database.
    """
    pass


class TaskAccessForbidden(Exception):
    """
    Raised when a user attempts to access or modify a task they do not own.
    """
    pass

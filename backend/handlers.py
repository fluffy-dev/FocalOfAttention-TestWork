"""
Defines centralized exception handlers for the FastAPI application.

These handlers catch specific custom exceptions raised throughout the
application (e.g., in the service or repository layers) and convert them
into standardized, user-friendly HTTP JSON responses with appropriate
status codes. This keeps the endpoint logic clean and free of repetitive
try/except blocks.
"""
from fastapi import Request, status
from fastapi.responses import JSONResponse

from backend.libs.exceptions import NotFound, AlreadyExists, PaginationError, AccessForbidden



async def not_found_exception_handler(request: Request, exc: NotFound):
    """Handles all exceptions inheriting from `libs.exceptions.NotFound`.

    This generic handler catches any exception that signifies a resource
    could not be found, such as `UserNotFound` or `TaskNotFound`, and
    returns a standard 404 Not Found response.

    Args:
        request (Request): The incoming FastAPI request object.
        exc (NotFound): The caught exception instance that inherits from the
            base `NotFound` class.

    Returns:
        JSONResponse: A JSON response with a 404 Not Found status code and a
            generic detail message.
    """
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": "The requested resource was not found."},
    )


async def already_exists_exception_handler(request: Request, exc: AlreadyExists):
    """Handles all exceptions inheriting from `libs.exceptions.AlreadyExists`.

    This handler is triggered when an attempt to create a resource fails
    because a resource with the same unique identifier (e.g., email) already
    exists in the database.

    Args:
        request (Request): The incoming FastAPI request object.
        exc (AlreadyExists): The caught exception instance that inherits from
            the base `AlreadyExists` class.

    Returns:
        JSONResponse: A JSON response with a 409 Conflict status code and a
            generic detail message.
    """
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": "A resource with the same unique identifier already exists."},
    )


async def access_forbidden_exception_handler(request: Request, exc: AccessForbidden):
    """Handles all exceptions inheriting from `libs.exceptions.AccessForbidden`.

    This handler catches permission-related errors, such as a user trying to
    access or modify a resource they do not own, and returns a standard
    403 Forbidden response.

    Args:
        request (Request): The incoming FastAPI request object.
        exc (AccessForbidden): The caught exception instance that inherits from
            the base `AccessForbidden` class.

    Returns:
        JSONResponse: A JSON response with a 403 Forbidden status code and a
            generic detail message.
    """
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={"detail": "You do not have permission to perform this action."},
    )


async def pagination_exception_handler(request: Request, exc: PaginationError):
    """Handles `PaginationError` exceptions for invalid limit/offset values.

    This handler is triggered if pagination parameters (like limit or offset)
    are provided with invalid values, such as negative numbers.

    Args:
        request (Request): The incoming FastAPI request object.
        exc (PaginationError): The caught exception instance.

    Returns:
        JSONResponse: A JSON response with a 400 Bad Request status code and a
            specific detail message about the pagination error.
    """
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": "Pagination limit and offset must be non-negative."},
    )


# Dictionary to be imported and registered in the main FastAPI application
exception_handlers = {
    NotFound: not_found_exception_handler,
    AlreadyExists: already_exists_exception_handler,
    AccessForbidden: access_forbidden_exception_handler,
    PaginationError: pagination_exception_handler,
}
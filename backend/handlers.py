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

from backend.libs.exceptions import NotFound, AlreadyExists, PaginationError
from backend.user.exceptions import UserAccessForbidden


async def not_found_exception_handler(request: Request, exc: NotFound):
    """
    Handles all exceptions inheriting from `libs.exceptions.NotFound`.

    Args:
        request (Request): The incoming request object.
        exc (NotFound): The caught exception instance.

    Returns:
        JSONResponse: A 404 Not Found response.
    """
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": "The requested resource was not found."},
    )


async def already_exists_exception_handler(request: Request, exc: AlreadyExists):
    """
    Handles all exceptions inheriting from `libs.exceptions.AlreadyExists`.

    Args:
        request (Request): The incoming request object.
        exc (AlreadyExists): The caught exception instance.

    Returns:
        JSONResponse: A 409 Conflict response.
    """
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": "A resource with the same unique identifier already exists."},
    )


async def access_forbidden_exception_handler(request: Request, exc: UserAccessForbidden):
    """
    Handles `UserAccessForbidden` exceptions.

    Args:
        request (Request): The incoming request object.
        exc (UserAccessForbidden): The caught exception instance.

    Returns:
        JSONResponse: A 403 Forbidden response.
    """
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={"detail": "You do not have permission to perform this action."},
    )


async def pagination_exception_handler(request: Request, exc: PaginationError):
    """
    Handles `PaginationError` exceptions for invalid limit/offset values.

    Args:
        request (Request): The incoming request object.
        exc (PaginationError): The caught exception instance.

    Returns:
        JSONResponse: A 400 Bad Request response.
    """
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": "Pagination limit and offset must be non-negative."},
    )


# Dictionary to be imported and registered in the main FastAPI application
exception_handlers = {
    NotFound: not_found_exception_handler,
    AlreadyExists: already_exists_exception_handler,
    UserAccessForbidden: access_forbidden_exception_handler,
    PaginationError: pagination_exception_handler,
}
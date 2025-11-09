"""Defines the RESTful API endpoints for full CRUD user management.

This module sets up the API routes for user-related operations. It delegates
all business logic to the `UserService` via dependency injection, keeping the
endpoint definitions clean and focused on the API contract (paths, methods,
request/response models).
"""
from typing import List

from fastapi import APIRouter, status

from backend.user.dependencies.service import IUserService
from backend.user.dto import (
    UserCreate, UserUpdate, UserDTO
)

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/",
    response_model=UserDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user"
)
async def create_user(
        user_data: UserCreate,
        service: IUserService,
):
    """Creates a new user account.

    This is a public endpoint for user registration. It will return a 409
    Conflict error if the username or email is already taken.

    Args:
        user_data (UserCreate): The user registration data from the request body.
        service (IUserService): The injected user service dependency.

    Returns:
        UserDTO: The newly created user's data.
    """
    return await service.create_user(user_data)


@router.get(
    "/",
    response_model=List[UserDTO],
    summary="Get a list of all users"
)
async def get_all_users(
        service: IUserService,
        limit: int = 100,
        offset: int = 0
):
    """Retrieves a paginated list of all users.

    This endpoint might be protected in a real-world scenario to be
    accessible only by admin users.

    Args:
        service (IUserService): The injected user service dependency.
        limit (int): The maximum number of users to return.
        offset (int): The number of users to skip for pagination.

    Returns:
        List[UserDTO]: A list of user data objects.
    """
    return await service.get_all_users(limit, offset)


@router.get(
    "/{user_id}",
    response_model=UserDTO,
    summary="Get a user's profile by ID"
)
async def get_user_by_id(
        user_id: int,
        service: IUserService,
):
    """Retrieves a specific user's profile by their ID.

    This endpoint will return a 404 Not Found if the user does not exist.

    Args:
        user_id (int): The ID of the user to retrieve.
        service (IUserService): The injected user service dependency.

    Returns:
        UserDTO: The requested user's data.
    """
    return await service.get_user_by_id(user_id)


@router.put(
    "/{user_id}",
    response_model=UserDTO,
    summary="Update a user's profile"
)
async def update_user(
        user_id: int,
        update_data: UserUpdate,
        service: IUserService,
):
    """Updates a user's profile.

    In a real application, this would be protected to ensure a user can only
    update their own profile, returning a 403 Forbidden error otherwise.

    Args:
        user_id (int): The ID of the user to update.
        update_data (UserUpdate): The new user data from the request body.
        service (IUserService): The injected user service dependency.

    Returns:
        UserDTO: The updated user's data.
    """
    return await service.update_user(user_id, update_data)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a user's profile"
)
async def delete_user(
        user_id: int,
        service: IUserService,
):
    """Deletes a user's profile.

    In a real application, this would be protected to ensure a user can only
    delete their own profile, returning a 403 Forbidden error otherwise. A
    successful deletion returns a 204 No Content response.

    Args:
        user_id (int): The ID of the user to delete.
        service (IUserService): The injected user service dependency.
    """
    await service.delete_user(user_id)
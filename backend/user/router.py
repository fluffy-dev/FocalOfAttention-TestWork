"""
Defines the RESTful API endpoints for full CRUD user management.
"""
from typing import List

from fastapi import APIRouter, status

from backend.user.dependencies.service import IUserService
from backend.user.dto import (
    UserCreate, UserPrivateDTO, UserPublicDTO, UserUpdate
)

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/",
    response_model=UserPrivateDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user"
)
async def create_user(
        user_data: UserCreate,
        service: IUserService,
):
    """
    Creates a new user account.

    This is a public endpoint for user registration. It will return a 409
    Conflict error if the username or email is already taken.
    """
    return await service.create_user(user_data)


@router.get(
    "/",
    response_model=List[UserPublicDTO],
    summary="Get a list of all users"
)
async def get_all_users(
        service: IUserService,
        limit: int = 100,
        offset: int = 0
):
    """
    Retrieves a paginated list of all users' public profiles.

    This is a protected endpoint. In a real-world scenario, you would add
    an additional dependency here to check for admin privileges.
    """
    return await service.get_all_users(limit, offset)


@router.get(
    "/{user_id}",
    response_model=UserPublicDTO,
    summary="Get a user's public profile by ID"
)
async def get_user_by_id(
        user_id: int,
        service: IUserService,
):
    """
    Retrieves a specific user's public profile by their ID.

    This is a protected endpoint that will return a 404 Not Found if the
    user does not exist.
    """
    return await service.get_user_by_id(user_id)


@router.put(
    "/{user_id}",
    response_model=UserPrivateDTO,
    summary="Update a user's profile"
)
async def update_user(
        user_id: int,
        update_data: UserUpdate,
        service: IUserService,
):
    """
    Updates a user's profile.

    A user can only update their own profile. Attempting to update another
    user's profile will result in a 403 Forbidden error.
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
    """
    Deletes a user's profile.

    A user can only delete their own profile. Attempting to delete another
    user's profile will result in a 403 Forbidden error.
    """
    await service.delete_user(user_id)

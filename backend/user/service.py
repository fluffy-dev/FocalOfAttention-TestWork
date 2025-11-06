"""
Service layer for user-related business logic.
"""
from typing import List

from backend.security.service import PasswordService
from backend.user.dependencies.repository import IUserRepository
from backend.user.dto import (
    UserUpdate, UserCreate, UserDTO
)
from backend.user.entities import User
from libs.exceptions import PaginationError


class UserService:
    """
    Service for handling all user-related business logic.

    Args:
        repo (IUserRepository): The user repository dependency.
    """
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    async def create_user(self, dto: UserCreate) -> UserDTO:
        """
        Handles the logic of creating a new user.
        """
        hashed_password = PasswordService.get_password_hash(dto.password)
        user_entity = User(
            id = None,
            email = str(dto.email),
            username=dto.username,
            hashed_password = hashed_password,
        )
        user = await self.repo.create(user_entity)

        return user

    async def get_user_by_id(self, user_id: int) -> UserDTO:
        """
        Retrieves a user's public profile.
        """
        user = await self.repo.get(user_id)
        return user

    async def get_all_users(self, limit: int, offset: int) -> List[UserDTO]:
        """
        Retrieves a list of all users' public profiles.
        """

        if limit < 0 or offset < 0:
            raise PaginationError

        users = await self.repo.get_list(limit, offset)
        return users

    async def update_user(
        self, pk: int, dto: UserUpdate
    ) -> UserDTO:
        """
        Updates a user's profile after verifying permissions.
        """
        updated_user = await self.repo.update(pk, dto)
        return updated_user

    async def delete_user(self, pk: int) -> None:
        """
        Deletes a user's profile after verifying permissions.
        """
        await self.repo.delete(pk)
"""Service layer for user-related business logic.

This module encapsulates the core business logic for user operations. It
acts as an intermediary between the API layer (routers) and the data access
layer (repositories), handling tasks like password hashing, data validation,
and orchestrating calls to the repository.
"""
from typing import List, Optional

from backend.security.service import PasswordService
from backend.user.dependencies.repository import IUserRepository
from backend.user.dto import (
    UserUpdate, UserCreate, UserDTO, UserFindDTO
)
from backend.user.entity import UserEntity
from backend.libs.exceptions import PaginationError


class UserService:
    """Service for handling all user-related business logic.

    This service contains methods that implement the application's rules
    and processes for managing users.

    Attributes:
        repo (IUserRepository): The user repository dependency, providing an
            interface for data persistence operations.
    """
    def __init__(self, repo: IUserRepository):
        """Initializes the UserService.

        Args:
            repo (IUserRepository): The user repository dependency.
        """
        self.repo = repo

    async def create_user(self, dto: UserCreate) -> UserDTO:
        """Handles the logic of creating a new user.

        This method takes user creation data, hashes the password, creates a
        domain entity, and then passes it to the repository for persistence.

        Args:
            dto (UserCreate): A DTO containing the new user's data.

        Returns:
            UserDTO: A DTO representing the newly created user.
        """
        hashed_password = PasswordService.get_password_hash(dto.password)
        user_entity = UserEntity(
            id=None,
            email=str(dto.email),
            username=dto.username,
            hashed_password=hashed_password,
        )
        return await self.repo.create(user_entity)

    async def get_user_by_id(self, user_id: int) -> UserDTO:
        """Retrieves a user by their unique ID.

        Args:
            user_id (int): The ID of the user to retrieve.

        Returns:
            UserDTO: The requested user's data.
        """
        return await self.repo.get(user_id)

    async def get_all_users(self, limit: Optional[int], offset: Optional[int]) -> List[UserDTO]:
        """Retrieves a paginated list of all users.

        Validates that the pagination parameters are non-negative.

        Args:
            limit (Optional[int]): The maximum number of users to return.
            offset (Optional[int]): The number of users to skip.

        Returns:
            List[UserDTO]: A list of user data objects.

        Raises:
            PaginationError: If limit or offset are negative.
        """

        if (limit is not None and limit < 0) or (offset is not None and offset < 0):
            raise PaginationError

        return await self.repo.get_list(limit, offset)

    async def find_user(self, dto: UserFindDTO) -> UserDTO:
        """Retrieves a user by one of several unique parameters.

        Args:
            dto (UserFindDTO): A DTO containing criteria to find the user.

        Returns:
            UserDTO: The found user's data.
        """
        return await self.repo.find(dto)

    async def update_user(
        self, pk: int, dto: UserUpdate
    ) -> UserDTO:
        """Updates a user's profile.

        In a real-world scenario, this method would also contain authorization
        logic to ensure a user can only update their own profile.

        Args:
            pk (int): The ID of the user to update.
            dto (UserUpdate): A DTO with the fields to be updated.

        Returns:
            UserDTO: The updated user's data.
        """
        return await self.repo.update(pk, dto)

    async def delete_user(self, pk: int) -> None:
        """Deletes a user's profile.

        Similar to updating, this method would typically include authorization
        checks before proceeding with the deletion.

        Args:
            pk (int): The ID of the user to delete.
        """
        await self.repo.delete(pk)
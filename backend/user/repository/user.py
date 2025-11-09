"""
This module contains the repository for user data access, which handles
all database operations related to the UserModel.
"""
from typing import Optional, List

from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from backend.config.database import ISession
from backend.user.exceptions import UserAlreadyExists, UserNotFound
from backend.user.dto import UserUpdate, UserDTO, UserFindDTO
from backend.user.entity import UserEntity
from backend.user.models.user import UserModel


class UserRepository:
    """Repository for user data access, operating with SQLAlchemy models.

    This class abstracts the database interactions for the `UserModel`. It
    provides a clean, asynchronous API for creating, retrieving, updating,
    and deleting user records. It is responsible for translating between
    domain entities/DTOs and the ORM model.

    Attributes:
        session (AsyncSession): The asynchronous SQLAlchemy session for
            database communication.
    """
    def __init__(self, session: ISession) -> None:
        """Initializes the UserRepository.

        Args:
            session (ISession): The database session dependency, which provides
                an `AsyncSession` for executing queries.
        """
        self.session: AsyncSession = session

    async def create(self, user: UserEntity) -> UserDTO:
        """Creates a new user record in the database.

        Args:
            user (User): A user domain entity containing the data for the new user.

        Returns:
            UserDTO: A data transfer object representing the newly created user.

        Raises:
            UserAlreadyExists: If a user with the same username or email
                already exists, violating a unique constraint.
        """
        instance = UserModel(
            username=user.username,
            email=str(user.email),
            hashed_password=user.hashed_password
        )
        self.session.add(instance)
        try:
            await self.session.commit()
            await self.session.refresh(instance)
            return self._get_dto(instance)
        except IntegrityError:
            await self.session.rollback()
            raise UserAlreadyExists

    async def get(self, pk: int) -> Optional[UserDTO]:
        """Retrieves a single user by their primary key.

        Args:
            pk (int): The unique ID of the user to retrieve.

        Returns:
            Optional[UserDTO]: A DTO of the found user.

        Raises:
            UserNotFound: If no user with the specified ID is found.
        """
        instance = await self.session.get(UserModel, pk)

        if instance is None:
            raise UserNotFound

        return self._get_dto(instance)

    async def find(self, dto: UserFindDTO) -> Optional[UserDTO]:
        """Finds a single user based on flexible criteria.

        Args:
            dto (UserFindDTO): A DTO containing one or more fields to filter
                by (e.g., id, username, email).

        Returns:
            Optional[UserDTO]: A DTO of the found user, if a unique match
                is found.

        Raises:
            UserNotFound: If no user matches the specified criteria.
        """
        stmt = select(UserModel).filter_by(**dto.model_dump(exclude_none=True))
        result = await self.session.execute(stmt)
        instance = result.scalar_one_or_none()
        if instance is None:
            raise UserNotFound
        return self._get_dto(instance)

    async def get_list(self, limit: int = 100, offset: int = 0) -> List[UserDTO]:
        """Retrieves a paginated list of users.

        Args:
            limit (int): The maximum number of users to return.
            offset (int): The number of users to skip from the beginning.

        Returns:
            List[UserDTO]: A list of user DTOs.
        """
        stmt = select(UserModel).offset(offset).limit(limit)
        result = await self.session.execute(stmt)
        instances = result.scalars().all()
        return [self._get_dto(instance) for instance in instances]

    async def update(self, pk: int, dto: UserUpdate) -> UserDTO:
        """Updates an existing user's record.

        Args:
            pk (int): The ID of the user to update.
            dto (UserUpdate): A DTO containing the fields to update.

        Returns:
            UserDTO: A DTO representing the updated state of the user.

        Raises:
            UserNotFound: If no user with the specified ID is found.
        """
        stmt = (
            update(UserModel)
            .values(**dto.model_dump(exclude_none=True))
            .where(UserModel.id == pk)
            .returning(UserModel)
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        instance = result.scalar_one_or_none()
        if instance is None:
            raise UserNotFound
        return self._get_dto(instance)

    async def delete(self, pk: int) -> None:
        """Deletes a user from the database.

        Args:
            pk (int): The ID of the user to delete.

        Raises:
            UserNotFound: If no user with the specified ID is found.
        """
        instance = await self.session.get(UserModel, pk)
        if instance is None:
            raise UserNotFound
        await self.session.delete(instance)
        await self.session.commit()

    @staticmethod
    def _get_dto(instance: UserModel) -> UserDTO:
        """Converts a UserModel ORM instance to a UserDTO.

        Args:
            instance (UserModel): The SQLAlchemy ORM model instance.

        Returns:
            UserDTO: The corresponding Pydantic data transfer object.
        """
        return UserDTO(
            id=instance.id,
            username=instance.username,
            email=instance.email,
            hashed_password=instance.hashed_password,
        )
"""
Repository for user data access, interacting with the database.

This layer is responsible for all CRUD (Create, Read, Update, Delete)
operations for the UserModel. It primarily returns DTOs to the service
layer but includes a secure mechanism to return ORM models when internal
access to fields like `hashed_password` is required by the calling service.
"""
from typing import overload, Union
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from backend.config.database import ISession
from backend.user.dto import UserDTO, UserFindDTO
from backend.user.entities import User
from backend.user.exceptions import UserAlreadyExists, UserNotFound
from backend.user.models.user import UserModel


class UserRepository:
    """
    Repository for user data access.

    Args:
        session (ISession): The database session dependency.
    """
    def __init__(self, session: ISession):
        self.session: AsyncSession = session

    @staticmethod
    def _to_dto(instance: UserModel) -> UserDTO:
        """Converts a UserModel SQLAlchemy instance to a UserDTO."""
        return UserDTO.model_validate(instance)

    async def create(self, user_entity: User) -> UserDTO:
        """
        Creates a new user record in the database from a domain entity.

        Args:
            user_entity (User): The domain entity containing the new user's data.

        Returns:
            UserDTO: The DTO of the newly created user.

        Raises:
            UserAlreadyExists: If a user with the same username or email
                already exists.
        """
        instance = UserModel(**user_entity.to_dict())
        self.session.add(instance)
        try:
            await self.session.commit()
            await self.session.refresh(instance)
            return self._to_dto(instance)
        except IntegrityError as e:
            await self.session.rollback()
            raise UserAlreadyExists from e

    @overload
    async def find(self, find_dto: UserFindDTO) -> UserDTO: ...

    @overload
    async def find(self, find_dto: UserFindDTO, *, return_model: bool = False) -> UserDTO: ...

    @overload
    async def find(self, find_dto: UserFindDTO, *, return_model: bool = True) -> UserModel: ...

    async def find(
        self, find_dto: UserFindDTO, *, return_model: bool = False
    ) -> Union[UserDTO, UserModel]:
        """
        Finds a single user based on flexible criteria.

        By default, this method returns a safe DTO. The `return_model` flag
        can be set to True to return the raw SQLAlchemy model, which should
        only be done for internal services like authentication that need to
        access sensitive fields not present in the DTO.

        Args:
            find_dto (UserFindDTO): DTO with optional fields (id, username,
                email) to search by.
            return_model (bool): If True, returns the SQLAlchemy UserModel
                instance instead of the UserDTO. Defaults to False.

        Returns:
            Union[UserDTO, UserModel]: The found user as a DTO or ORM model.

        Raises:
            UserNotFound: If no user matches the provided criteria.
            ValueError: If no search criteria are provided.
        """
        criteria = find_dto.model_dump(exclude_none=True)
        if not criteria:
            raise ValueError("At least one search criterion must be provided.")

        stmt = select(UserModel).filter_by(**criteria)
        result = await self.session.execute(stmt)
        instance = result.scalar_one_or_none()

        if instance is None:
            raise UserNotFound

        return instance if return_model else self._to_dto(instance)
from typing import Optional, List

from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError

from backend.config.database import ISession
from backend.user.exceptions import UserAlreadyExists, UserNotFound
from backend.user.dto import UserUpdate, UserDTO, UserFindDTO
from backend.user.entities import User
from backend.user.models.user import UserModel


class UserRepository:
    """
    Repository for user data access, operating with DTOs.
    """
    def __init__(self, session: ISession) -> None:
        self.session: ISession = session

    async def create(self, user: User) -> UserDTO:
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
        instance = await self.session.get(UserModel, pk)

        if instance is None:
            raise UserNotFound

        return self._get_dto(instance)

    async def find(self, dto: UserFindDTO) -> Optional[UserDTO]:
        stmt = select(UserModel).filter_by(**dto.model_dump(exclude_none=True))
        result = await self.session.execute(stmt)
        instance = result.scalar_one_or_none()
        if instance is None:
            raise UserNotFound
        return self._get_dto(instance)

    async def get_list(self, limit: int = 100, offset: int = 0) -> List[UserDTO]:
        stmt = select(UserModel).offset(offset).limit(limit)
        result = await self.session.execute(stmt)
        instances = result.scalars().all()
        return [self._get_dto(instance) for instance in instances]

    async def update(self, pk: int, dto: UserUpdate) -> UserDTO:
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
        """
        Deletes a user from the database.

        Args:
            pk (int): The ID of the user to delete.
        """
        instance = await self.session.get(UserModel, pk)
        if instance is None:
            raise UserNotFound
        await self.session.delete(instance)
        await self.session.commit()

    @staticmethod
    def _get_dto(instance: UserModel) -> UserDTO:
        return UserDTO(
            id=instance.id,
            username=instance.username,
            email=instance.email,
            hashed_password=instance.hashed_password,
        )

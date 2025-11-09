"""
Repository for task data access.
"""
from typing import List, Optional
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from backend.config.database import ISession
from backend.task.dto import TaskCreate, TaskUpdate, TaskDTO
from backend.task.exceptions import TaskNotFound
from backend.task.models.task import TaskModel, TaskStatus


class TaskRepository:
    """
    Repository for task data access, operating with SQLAlchemy models.

    Args:
        session (ISession): The database session dependency.
    """
    def __init__(self, session: ISession):
        self.session: AsyncSession = session

    async def create(self, task_create: TaskCreate, owner_id: int) -> TaskDTO:
        """
        Creates a new task record in the database.

        Args:
            task_create (TaskCreate): DTO with the data for the new task.
            owner_id (int): The ID of the user who owns the task.

        Returns:
            TaskDTO: The newly created SQLAlchemy task model Pydantic instance.
        """
        instance = TaskModel(**task_create.model_dump(), owner_id=owner_id)
        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)
        return self._get_dto(instance)

    async def get_by_id(self, task_id: int) -> TaskDTO:
        """
        Retrieves a task by its ID.

        Args:
            task_id (int): The ID of the task to retrieve.

        Returns:
            TaskDTO: The SQLAlchemy model Pydantic instance for the task.

        Raises:
            TaskNotFound: If no task with the specified ID is found.
        """
        instance = await self.session.get(TaskModel, task_id)

        if instance is None:
            raise TaskNotFound

        return self._get_dto(instance)

    async def get_all_for_user(
        self, owner_id: int, status: Optional[TaskStatus] = None
    ) -> List[TaskDTO]:
        """
        Retrieves all tasks for a specific user, with optional status filtering.

        Args:
            owner_id (int): The ID of the user whose tasks to retrieve.
            status (Optional[TaskStatus]): If provided, filters tasks by this status.

        Returns:
            List[TaskDTO]: A list of task model instances.
        """
        stmt = select(TaskModel).where(TaskModel.owner_id == owner_id)
        if status:
            stmt = stmt.where(TaskModel.status == status)
        result = await self.session.execute(stmt)
        instances = result.scalars().all()
        return [self._get_dto(instance) for instance in instances]

    async def update(self, task_id: int, dto: TaskUpdate) -> TaskDTO:
        """
        Updates an existing task with new data.

        Args:
            task_id (int): The ID of the task to update.
            dto (TaskUpdate): A DTO containing the fields to update.

        Returns:
            TaskDTO: The updated SQLAlchemy task model Pydantic instance.
        """
        stmt = update(TaskModel).values(**dto.model_dump()).filter_by(id=task_id).returning(TaskModel)
        raw = await self.session.execute(stmt)
        instance = raw.scalar_one_or_none()
        await self.session.commit()

        if instance is None:
            raise TaskNotFound

        return self._get_dto(instance)

    async def delete(self, task_id: int) -> None:
        """
        Deletes a task from the database.

        Args:
            task_id (int): The ID of the task to delete.
        """
        stmt = delete(TaskModel).where(TaskModel.id == task_id)
        await self.session.execute(stmt)
        await self.session.commit()

    def _get_dto(self, instance: TaskModel) -> TaskDTO:
        """
        Helper function to transform a SQLAlchemy model instance into a TaskDTO.

        Args:
            instance (TaskModel): The SQLAlchemy model instance.

        Returns:
            TaskDTO: The Pydantic object representing the task.
        """

        return TaskDTO(
            id=instance.id,
            title=instance.title,
            description=instance.description,
            status=instance.status,
            owner_id=instance.owner_id,
        )

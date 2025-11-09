"""
Repository for task data access.
"""
from typing import List, Optional
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from backend.config.database import ISession

from backend.task.entity import TaskEntity
from backend.task.exceptions import TaskNotFound
from backend.task.dto import TaskUpdate, TaskDTO
from backend.task.models.task import TaskModel, TaskStatus


class TaskRepository:
    """Repository for task data access, operating with SQLAlchemy models.

    This class provides a low-level interface for interacting with the task
    data storage. It encapsulates the direct database operations for creating,
    retrieving, updating, and deleting tasks using an asynchronous SQLAlchemy
    session. This layer is not responsible for business logic like ownership
    verification.

    Attributes:
        session (AsyncSession): The database session for executing queries.
    """

    def __init__(self, session: ISession):
        """Initializes the TaskRepository.

        Args:
            session (ISession): The database session dependency, which should be
                an instance of an asynchronous session manager that provides an
                AsyncSession for database interactions.
        """
        self.session: AsyncSession = session

    async def create(self, entity: TaskEntity) -> TaskDTO:
        """Creates a new task record in the database.

        This method takes a TaskEntity, which contains the data for a new task,
        creates a new TaskModel instance, and persists it to the database.

        Args:
            entity (TaskEntity): A dataclass instance containing the data for the
                new task, including owner_id, title, and description.

        Returns:
            TaskDTO: A Pydantic data transfer object representing the newly
                created task, including all its database-generated attributes
                like id and default status.
        """
        instance = TaskModel(
            owner_id=entity.owner_id,
            title=entity.title,
            description=entity.description,
        )
        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)
        return self._get_dto(instance)

    async def get_by_id(self, task_id: int) -> TaskDTO:
        """Retrieves a task by its unique identifier.

        Args:
            task_id (int): The primary key of the task to retrieve.

        Returns:
            TaskDTO: A Pydantic data transfer object for the found task.

        Raises:
            TaskNotFound: If no task with the specified ID exists in the
                database.
        """
        instance = await self.session.get(TaskModel, task_id)

        if instance is None:
            raise TaskNotFound

        return self._get_dto(instance)

    async def get_all_for_user(
        self, owner_id: int, status: Optional[TaskStatus] = None
    ) -> List[TaskDTO]:
        """Retrieves all tasks for a specific user.

        This method can optionally filter the tasks by their status.

        Args:
            owner_id (int): The ID of the user whose tasks are to be retrieved.
            status (Optional[TaskStatus]): An optional enum member to filter
                tasks by their status (e.g., PENDING, IN_PROGRESS, COMPLETED).
                If None, tasks of all statuses are returned.

        Returns:
            List[TaskDTO]: A list of Pydantic data transfer objects, each
                representing a task belonging to the specified user.
        """
        stmt = select(TaskModel).where(TaskModel.owner_id == owner_id)

        if status:
            stmt = stmt.where(TaskModel.status == status)

        result = await self.session.execute(stmt)
        instances = result.scalars().all()
        return [self._get_dto(instance) for instance in instances]

    async def update(self, task_id: int, dto: TaskUpdate) -> TaskDTO:
        """Updates an existing task with new data.

        This method applies updates from a TaskUpdate DTO to a task specified
        by its primary key.

        Args:
            task_id (int): The ID of the task to update.
            dto (TaskUpdate): A Pydantic data transfer object containing the
                fields to be updated.

        Returns:
            TaskDTO: A Pydantic data transfer object representing the updated
                task.

        Raises:
            TaskNotFound: If no task with the specified ID is found.
        """
        stmt = update(TaskModel).values(**dto.model_dump(exclude_none=True)).filter_by(id=task_id).returning(TaskModel)
        raw = await self.session.execute(stmt)
        instance = raw.scalar_one_or_none()
        await self.session.commit()

        if instance is None:
            raise TaskNotFound

        return self._get_dto(instance)

    async def delete(self, task_id: int) -> None:
        """Deletes a task from the database.

        This method deletes a task based on its primary key.

        Args:
            task_id (int): The ID of the task to be deleted.
        """
        stmt = delete(TaskModel).where(TaskModel.id == task_id)
        await self.session.execute(stmt)
        await self.session.commit()

    def _get_dto(self, instance: TaskModel) -> TaskDTO:
        """Transforms a SQLAlchemy TaskModel instance into a TaskDTO.

        This is a private helper method used to convert database model objects
        into Pydantic DTOs for consistent data structuring in the application.

        Args:
            instance (TaskModel): The SQLAlchemy model instance of a task.

        Returns:
            TaskDTO: A Pydantic data transfer object representing the task's
                data.
        """

        return TaskDTO(
            id=instance.id,
            title=instance.title,
            description=instance.description,
            status=instance.status,
            owner_id=instance.owner_id,
        )
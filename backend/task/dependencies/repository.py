from fastapi import Depends
from typing import Annotated

from backend.task.repository.task import TaskRepository

ITaskRepository: type[TaskRepository] = Annotated[TaskRepository, Depends()]
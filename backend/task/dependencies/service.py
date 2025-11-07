from fastapi import Depends
from typing import Annotated

from backend.task.service import TaskService

ITaskService: type[TaskService] = Annotated[TaskService, Depends()]
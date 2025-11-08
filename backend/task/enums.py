from enum import Enum


class TaskStatus(Enum):
    """Enumeration for the possible statuses of a task."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    DONE = "done"
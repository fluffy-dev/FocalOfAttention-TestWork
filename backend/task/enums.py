from enum import Enum


class TaskStatus(str, Enum):
    """Enumeration for the possible statuses of a task.

    This class defines a fixed set of statuses that a task can be in
    throughout its lifecycle. Using an enum ensures that the status field
    in the database and in the application's logic is always one of these
    predefined values, preventing data inconsistency from typos or invalid
    states.

    By inheriting from `str`, the enum members behave like strings, which
    makes them easily serializable for API responses and database storage.

    Attributes:
        PENDING (str): The initial state of a task after creation, before any
            work has begun.
        IN_PROGRESS (str): Represents a task that is actively being worked on.
        DONE (str): The final state of a task, indicating that it has been
            completed.
    """
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    DONE = "done"
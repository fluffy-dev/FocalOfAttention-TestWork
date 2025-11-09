"""
it's entity for task creation, it like layer between service and repo, or router and repo
"""
from dataclasses import dataclass


@dataclass
class TaskEntity:
    """Represents the essential data needed to create a new task.

    This dataclass acts as an internal, domain-focused object. It serves as a
    clean data structure to transfer the information required for task creation
    between different layers of the application, typically from the service layer
    to the repository layer.

    Using an entity like this helps to decouple the persistence layer (repository)
    from the API layer's Data Transfer Objects (DTOs), ensuring that the
    repository only receives the exact data it needs in a simple, predictable
    format, free from API-specific validation or details.

    Attributes:
        owner_id (int): The unique identifier of the user who will own the task.
        title (str): The title for the new task.
        description (str): The detailed description for the new task.
    """
    owner_id: int
    title: str
    description: str
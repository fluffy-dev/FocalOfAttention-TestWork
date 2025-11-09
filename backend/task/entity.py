from dataclasses import dataclass


@dataclass
class TaskEntity:
    owner_id: int
    title: str
    description: str

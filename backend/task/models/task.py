"""
Defines the SQLAlchemy ORM model for tasks.
"""
import enum
from typing import TYPE_CHECKING
from sqlalchemy import String, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.libs.base_model import Base
from backend.task.enums import TaskStatus

if TYPE_CHECKING:
    from backend.user.models.user import UserModel


class TaskModel(Base):
    """
    SQLAlchemy model for a task.

    Each task has a title, an optional description, a status, and a mandatory
    link to the user who owns it.

    Attributes:
        title (Mapped[str]): The title of the task.
        description (Mapped[str | None]): A more detailed description of the task.
        status (Mapped[TaskStatus]): The current status of the task.
        owner_id (Mapped[int]): The foreign key linking to the user owner.
        owner (Mapped["UserModel"]): The ORM relationship to the owning user.
    """
    __tablename__ = "tasks"

    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(String, nullable=True)
    status: Mapped[TaskStatus] = mapped_column(
        Enum(TaskStatus),
        default=TaskStatus.PENDING,
        nullable=False
    )
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    owner: Mapped["UserModel"] = relationship(back_populates="tasks")
"""Defines the SQLAlchemy ORM model for users.

This module contains the `UserModel`, which maps the `users` table in the
database to a Python class. It defines the table structure, columns, and
relationships to other models, serving as the primary interface for database
interactions concerning user data via the ORM.
"""
from typing import List, TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.libs.base_model import Base

if TYPE_CHECKING:
    from task.models.task import TaskModel


class UserModel(Base):
    """SQLAlchemy ORM model for a user.

    This class represents the `users` table in the database. Each instance
    of this class corresponds to a single row in the table.

    Attributes:
        username (Mapped[str]): The user's unique login name, indexed for
            fast lookups.
        email (Mapped[str]): The user's unique email address, also indexed.
        hashed_password (Mapped[str]): The user's securely hashed password.
        tasks (Mapped[List["TaskModel"]]): A one-to-many relationship to the
            tasks owned by this user. The `back_populates` argument ensures
            that the relationship is bidirectionally linked with the `owner`
            attribute on the `TaskModel`.
    """
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))

    tasks: Mapped[List["TaskModel"]] = relationship(back_populates="owner")
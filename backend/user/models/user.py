"""
Defines the SQLAlchemy ORM model for users.
"""
from typing import List
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.libs.base_model import Base


class UserModel(Base):
    """
    SQLAlchemy model for a user.

    Attributes:
        username (Mapped[str]): The user's unique login name.
        email (Mapped[str]): The user's unique email address.
        hashed_password (Mapped[str]): The user's securely hashed password.
        tasks (Mapped[List["TaskModel"]]): A relationship to the tasks
            owned by this user.
    """
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))

    tasks: Mapped[List["TaskModel"]] = relationship(back_populates="owner")
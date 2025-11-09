"""Defines Data Transfer Objects (DTOs) for the User module using Pydantic.

These models are used for data validation in API requests, serialization in
API responses, and as structured data containers between application layers.
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserDTO(BaseModel):
    """DTO for representing a user's data.

    This model represents a user as stored in the system, including the
    hashed password. It's intended for internal use between layers (e.g.,
    repository to service) and for API responses where appropriate, although
    exposing the hashed password should be done with care.

    Attributes:
        id (int): The unique identifier for the user.
        username (str): The user's unique username.
        email (EmailStr | str): The user's unique email address.
        hashed_password (str): The stored hashed password for the user.
    """

    id: int = Field(..., description="The unique identifier for the user.")
    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="The unique username for the user."
    )
    email: EmailStr | str = Field(..., description="The unique email address for the user.")
    hashed_password: str = Field(..., description="The hashed password for the user.")

    class Config:
        """Pydantic configuration to allow ORM model mapping.

        The `from_attributes = True` setting enables creating an instance of this
        DTO directly from a SQLAlchemy ORM model instance.
        """
        from_attributes = True

class UserUpdate(BaseModel):
    """DTO for updating a user's profile. All fields are optional.

    This model is used to validate the payload for a user update request.
    Since all fields are optional, it supports partial updates.

    Attributes:
        username (Optional[str]): A new username. Must be 3-50 characters.
        email (Optional[EmailStr]): A new, valid email address.
        password (Optional[str]): A new password. Must be at least 8 characters.
    """
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(
        None,
        min_length=8,
        description="A new password. If provided, it must be at least 8 characters."
    )

class UserCreate(BaseModel):
    """DTO for creating a new user. Used to validate registration requests.

    Attributes:
        username (str): The username for the new account (3-50 characters).
        email (EmailStr): The email address for the new account.
        password (str): The plaintext password (min 8 characters).
    """
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)


class UserFindDTO(BaseModel):
    """DTO for flexibly searching for a user.

    All fields are optional, allowing the service layer to find a user
    by any combination of these unique identifiers. This is used internally
    by services and not exposed directly as an API endpoint body.

    Attributes:
        id (Optional[int]): Find user by their unique ID.
        username (Optional[str]): Find user by their username.
        email (Optional[EmailStr]): Find user by their email.
    """
    id: Optional[int] = Field(None, description="Find user by their unique ID.")
    username: Optional[str] = Field(None, description="Find user by their username.")
    email: Optional[EmailStr] = Field(None, description="Find user by their email.")
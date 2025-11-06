"""
Defines Data Transfer Objects (DTOs) for the User module using Pydantic.

These models are used for data validation in API requests, serialization in
API responses, and as structured data containers between application layers.
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserDTO(BaseModel):
    """
    DTO for representing a user's data in API responses.

    This model represents a user as stored in the system, excluding any
    sensitive information like the password. It includes the user's ID.
    """

    id: int = Field(..., description="The unique identifier for the user.")
    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="The unique username for the user."
    )
    email: EmailStr = Field(..., description="The unique email address for the user.")

    class Config:
        """Pydantic configuration to allow ORM model mapping."""
        from_attributes = True

class UserUpdate(BaseModel):
    """
    DTO for updating a user's profile. All fields are optional.
    """
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(
        None,
        min_length=8,
        description="A new password. If provided, it must be at least 8 characters."
    )

class UserPrivateDTO(BaseModel):
    """
    DTO for a user's private profile, including personal details like email.
    """

    id: int = Field(..., description="The unique identifier for the user.")
    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="The unique username for the user."
    )
    email: EmailStr = Field(..., description="The unique email address for the user.")

    class Config:
        """Pydantic configuration to allow ORM model mapping."""
        from_attributes = True


class UserPublicDTO(BaseModel):
    """
    DTO for a user's public profile. Excludes sensitive information.
    """
    id: int
    username: str

    class Config:
        """Pydantic configuration to allow ORM model mapping."""
        from_attributes = True

class UserFindDTO(BaseModel):
    """
    DTO for flexibly searching for a user.

    All fields are optional, allowing the service layer to find a user
    by any combination of these unique identifiers. This is used internally
    by services and not exposed directly as an API endpoint body.
    """
    id: Optional[int] = Field(None, description="Find user by their unique ID.")
    username: Optional[str] = Field(None, description="Find user by their username.")
    email: Optional[EmailStr] = Field(None, description="Find user by their email.")
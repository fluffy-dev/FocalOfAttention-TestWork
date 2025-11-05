"""
Defines Data Transfer Objects (DTOs) for the User module.
"""
from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    """
    Base DTO for user data, containing shared fields.
    """
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr


class UserCreate(UserBase):
    """
    DTO for creating a new user. Includes password validation.
    """
    password: str = Field(..., min_length=8)


class UserDTO(UserBase):
    """
    DTO for representing a user's data, excluding the password.

    Used for API responses to avoid exposing sensitive information.
    """
    id: int

    class Config:
        from_attributes = True
"""
Defines Data Transfer Objects (DTOs) for the Authentication module.
"""
from pydantic import BaseModel, EmailStr, Field


class RegistrationDTO(BaseModel):
    """
    DTO for handling a new user registration request.

    This model validates the data required to create a new user account.
    """
    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="The desired unique username."
    )
    email: EmailStr = Field(..., description="The user's unique email address.")
    password: str = Field(
        ...,
        min_length=8,
        description="A secure password for the new account (min 8 characters)."
    )


class LoginDTO(BaseModel):
    """
    DTO for handling a user login request.

    This model is used to validate the credentials provided by a user
    when they attempt to log in.
    """
    username: str = Field(..., description="The user's username.")
    password: str = Field(..., description="The user's password.")
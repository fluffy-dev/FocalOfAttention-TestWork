"""
Authentication and security configuration.

This module uses pydantic-settings to load all security-related
parameters, such as the JWT secret key, algorithm, and token lifetimes,
from environment variables.
"""
from pydantic import Field
from pydantic_settings import BaseSettings


class AuthConfig(BaseSettings):
    """
    Configuration for authentication and security.

    Attributes:
        secret_key (str): The secret key for signing JWTs.
        algorithm (str): The algorithm used for JWT hashing (e.g., "HS256").
        access_token_expire_minutes (int): The lifetime of an access token.
        refresh_token_expire_days (int): The lifetime of a refresh token.
    """
    secret_key: str = Field(..., alias="SECRET_KEY")
    algorithm: str = Field("HS256", alias="HASH_ALGORITHM")
    access_token_expire_minutes: int = Field(30, alias="ACCESS_TOKEN_EXPIRE_MINUTES")
    refresh_token_expire_days: int = Field(7, alias="REFRESH_TOKEN_EXPIRE_DAYS")

auth_config = AuthConfig()
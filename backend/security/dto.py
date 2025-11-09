"""
Defines Data Transfer Objects (DTOs) for the Security module.

This module contains the Pydantic models used for handling authentication tokens
and their payloads. These DTOs provide a clear, validated structure for token-related
data as it is passed between the application and the client, or used internally
for encoding and decoding JSON Web Tokens (JWTs).
"""
from pydantic import BaseModel


class TokenDTO(BaseModel):
    """DTO for representing JWT access and refresh tokens.

    This model defines the standard response format for a successful
    authentication request. It bundles the access token, which is used for
    authorizing subsequent API requests, and the refresh token, which can be
    used to obtain a new access token without requiring the user to log in again.

    Attributes:
        access_token (str): The JSON Web Token (JWT) used to authenticate the
            user for protected endpoints.
        refresh_token (str): The token used to obtain a new access token once
            the current one expires.
        token_type (str): The type of the token, which is almost always
            "bearer" for JWT-based authentication. Defaults to "bearer".
    """
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenPayloadDTO(BaseModel):
    """DTO for the payload data encoded within the JWT.

    This model represents the claims contained within the JWT payload. It is
    used to validate the structure of the decoded token data to ensure it
    contains the necessary information, such as the subject (user identifier).

    Attributes:
        sub (str | None): The 'subject' of the token, as defined in the JWT
            standard (RFC 7519). This field typically contains the unique
            identifier of the user (e.g., user ID or username) to whom the
            token was issued. Defaults to None.
    """
    sub: str | None = None
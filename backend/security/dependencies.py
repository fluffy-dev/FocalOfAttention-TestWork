"""
Defines FastAPI dependencies for security and user authentication.

This module provides the `ICurrentUser` dependency, which is the standard
mechanism for protecting endpoints and retrieving the currently authenticated
user's data. It uses the standard OAuth2 "Bearer" token flow.
"""
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from backend.security.service import TokenService
from backend.user.dependencies.repository import IUserRepository
from backend.user.dto import UserDTO, UserFindDTO
from backend.user.exceptions import UserNotFound


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/auth/login")

IToken = Annotated[str, Depends(oauth2_scheme)]


async def get_current_user(token: IToken, user_repo: IUserRepository) -> UserDTO:
    """
    A dependency to retrieve the current user from a JWT Bearer token.

    This function is the heart of the authentication system for protected
    endpoints. It depends on `oauth2_scheme` to get the token string from the
    request header, then validates it and fetches the corresponding user.

    Args:
        token (IToken): The Bearer token string automatically extracted from
            the Authorization header by the `oauth2_scheme` dependency.
        user_repo (IUserRepository): The user repository dependency, injected by FastAPI.

    Returns:
        UserDTO: The data of the authenticated user.

    Raises:
        HTTPException(401): If the token is invalid, expired, or the user
            it references no longer exists.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = TokenService.verify_token(token)
    if payload is None or payload.sub is None:
        raise credentials_exception

    try:
        user_id: int = int(payload.sub)

        user = await user_repo.find(UserFindDTO(id=user_id))
        return user
    except (UserNotFound, ValueError):
        raise credentials_exception


ICurrentUser: type[UserDTO] = Annotated[UserDTO, Depends(get_current_user)]
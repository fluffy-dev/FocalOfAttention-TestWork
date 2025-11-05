"""
Defines FastAPI dependencies for security and user authentication.
"""
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from backend.security.service import TokenService
from backend.user.dependencies.repository import IUserRepository
from backend.user.dto import UserDTO, UserFindDTO
from backend.user.exceptions import UserNotFound

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")
IToken = Annotated[str, Depends(oauth2_scheme)]


async def get_current_user(token: IToken, user_repo: IUserRepository) -> UserDTO:
    """
    Dependency to get the current authenticated user from a JWT token.

    Verifies the token, extracts the user ID, and fetches the user's safe DTO
    from the repository.

    Args:
        token (IToken): The bearer token from the request.
        user_repo (IUserRepository): The user repository dependency.

    Returns:
        UserDTO: The data of the authenticated user.

    Raises:
        HTTPException(401): If the token is invalid or the user is not found.
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

ICurrentUser = Annotated[UserDTO, Depends(get_current_user)]
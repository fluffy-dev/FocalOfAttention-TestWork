"""
Defines the RESTful API endpoints for user authentication and registration.
"""
from typing import Annotated
from fastapi import APIRouter, Depends, Form, HTTPException, status

from backend.auth.dto import RegistrationDTO, LoginDTO
from backend.security.dto import TokenDTO
from backend.auth.dependencies.service import IAuthService
from backend.user.exceptions import UserNotFound


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=TokenDTO,
    summary="Register a new user and get tokens"
)
async def register(
    registration_data: RegistrationDTO,
    service: IAuthService,
):
    """
    Creates a new user account and returns a set of access and refresh
    tokens for immediate authentication.
    """
    return await service.register(registration_data)


@router.post(
    "/login",
    response_model=TokenDTO,
    summary="Log in to get access and refresh tokens"
)
async def login(
    login_data: LoginDTO,
    service: IAuthService,
):
    """
    Authenticates a user with their username and password and returns a set
    of access and refresh tokens.
    """
    try:
        return await service.login(login_data)
    except UserNotFound:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )


@router.post(
    "/refresh",
    response_model=TokenDTO,
    summary="Refresh access and refresh tokens"
)
async def refresh(
    refresh_token: Annotated[str, Form()],
    service: IAuthService,
):
    """
    Issues a new pair of tokens if a valid refresh token is provided.
    """
    try:
        return await service.refresh_tokens(refresh_token)
    except UserNotFound:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token or user not found",
        )
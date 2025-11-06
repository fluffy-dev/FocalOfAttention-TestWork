"""
Defines the RESTful API endpoints for user authentication and registration.
"""
from fastapi import APIRouter, Depends

from backend.auth.dto import RegistrationDTO, LoginDTO
from backend.security.dto import TokenDTO
from backend.auth.dependencies.service import IAuthService


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
    return await service.login(login_data)
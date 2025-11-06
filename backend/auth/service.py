"""
Service layer for authentication business logic, including registration and login.
"""
from backend.user.dependencies.service import IUserService
from backend.user.dto import UserCreate, UserFindDTO
from backend.user.exceptions import UserNotFound
from backend.security.service import PasswordService, TokenService
from backend.security.dto import TokenDTO
from backend.auth.dto import RegistrationDTO, LoginDTO


class AuthService:
    """
    Service for handling user registration and authentication.

    This service orchestrates the user creation process via the UserService
    and handles credential verification for issuing JWTs.

    Args:
        user_service (IUserService): The user service dependency.
    """
    def __init__(self, user_service: IUserService):
        self.user_service = user_service

    async def register(self, dto: RegistrationDTO) -> TokenDTO:
        """
        Handles new user registration and immediately issues JWT tokens.

        Args:
            dto (RegistrationDTO): The registration data from the user.

        Returns:
            TokenDTO: A DTO containing the access and refresh tokens for the
                newly created and logged-in user.
        """
        user_create_dto = UserCreate(
            username=dto.username,
            email=dto.email,
            password=dto.password
        )
        new_user = await self.user_service.create_user(user_create_dto)

        access_token = TokenService.create_access_token(data={"sub": str(new_user.id)})
        refresh_token = TokenService.create_refresh_token(data={"sub": str(new_user.id)})

        return TokenDTO(access_token=access_token, refresh_token=refresh_token)

    async def login(self, dto: LoginDTO) -> TokenDTO:
        """
        Authenticates an existing user and issues JWT tokens.

        Args:
            dto (LoginDTO): The user's login credentials.

        Returns:
            TokenDTO: A DTO containing the access and refresh tokens.

        Raises:
            UserNotFound: If the username does not exist or the password
                is incorrect.
        """
        find_dto = UserFindDTO(username=dto.username)
        user = await self.user_service.find_user(find_dto)

        if not PasswordService.verify_password(dto.password, user.hashed_password):
            raise UserNotFound("Incorrect username or password")

        access_token = TokenService.create_access_token(data={"sub": str(user.id)})
        refresh_token = TokenService.create_refresh_token(data={"sub": str(user.id)})

        return TokenDTO(access_token=access_token, refresh_token=refresh_token)
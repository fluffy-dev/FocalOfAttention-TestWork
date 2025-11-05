"""
Service layer for authentication business logic.
"""
from fastapi.security import OAuth2PasswordRequestForm

from backend.user.dependencies.repository import IUserRepository
from backend.user.dto import UserFindDTO
from backend.user.exceptions import UserNotFound
from backend.security.service import PasswordService, TokenService
from backend.security.dto import TokenDTO


class AuthService:
    """
    Service for handling authentication logic, such as user login.

    Args:
        user_repo (IUserRepository): The user repository dependency.
    """
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    async def login(self, form_data: OAuth2PasswordRequestForm) -> TokenDTO:
        """
        Authenticates a user and issues JWT tokens.

        This method retrieves the full user model to access the hashed
        password for verification.

        Args:
            form_data (OAuth2PasswordRequestForm): The user's login and password.

        Returns:
            TokenDTO: A DTO containing the access and refresh tokens.

        Raises:
            UserNotFound: If the user does not exist or password is incorrect.
        """
        try:
            find_dto = UserFindDTO(username=form_data.username)
            user_model = await self.user_repo.find(find_dto, return_model=True)
        except UserNotFound:
            raise UserNotFound("Incorrect username or password")

        if not PasswordService.verify_password(form_data.password, user_model.hashed_password):
            raise UserNotFound("Incorrect username or password")

        access_token = TokenService.create_access_token(data={"sub": str(user_model.id)})
        refresh_token = TokenService.create_refresh_token(data={"sub": str(user_model.id)})

        return TokenDTO(access_token=access_token, refresh_token=refresh_token)
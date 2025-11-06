from fastapi import Depends
from typing import Annotated

from backend.auth.service import AuthService

IAuthService: type[AuthService] = Annotated[AuthService, Depends()]
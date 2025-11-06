from fastapi import Depends
from typing import Annotated

from backend.user.service import UserService

IUserService: type[UserService] = Annotated[UserService, Depends()]
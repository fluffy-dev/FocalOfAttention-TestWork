from fastapi import Depends
from typing import Annotated

from backend.user.repository.user import UserRepository


IUserRepository: type[UserRepository] = Annotated[UserRepository, Depends()]
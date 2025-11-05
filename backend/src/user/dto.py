from typing import Optional, Annotated
from pydantic import BaseModel, EmailStr, StringConstraints

class UserDTO(BaseModel):
    id: Optional[int] = None
    name: Annotated[str, StringConstraints(max_length=30)]
    login: Annotated[str, StringConstraints(max_length=50)]
    email: EmailStr
    password: Optional[str] = None

class FindUserDTO(BaseModel):
    id: Optional[int] = None
    login: Optional[Annotated[str, StringConstraints(max_length=50)]] = None
    email: Optional[EmailStr] = None

class UpdateUserDTO(BaseModel):
    name: Optional[Annotated[str, StringConstraints(max_length=30)]] = None
    login: Optional[Annotated[str, StringConstraints(max_length=50)]] = None
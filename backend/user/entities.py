"""
Defines the domain entities for the User module.

Entities are simple dataclasses that represent the core business objects
of the application. They are decoupled from the database (ORM models) and
the API (DTOs), containing only data and business logic-related methods.
"""
from dataclasses import dataclass, asdict


@dataclass
class User:
    """
    Represents a user within the application's domain.

    This entity holds the core attributes of a user, including sensitive
    data like the hashed password, which is necessary for business logic
    but should never be exposed in DTOs.

    Attributes:
        id (int | None): The unique identifier for the user, or None if new.
        username (str): The user's unique username.
        email (str): The user's unique email address.
        hashed_password (str): The user's securely hashed password.
    """
    id: int | None
    username: str
    email: str
    hashed_password: str

    def to_dict(self):
        """Converts the dataclass instance to a dictionary."""
        return asdict(self)
"""
Provides core services for security-related operations like password
hashing/verification and JWT creation/validation.
"""
from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from backend.config.auth_settings import auth_config
from backend.security.dto import TokenPayloadDTO

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class PasswordService:
    """
    Provides static methods for password hashing and verification.
    """
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Verifies a plain password against its hashed version.

        Args:
            plain_password (str): The password attempt.
            hashed_password (str): The stored hashed password.

        Returns:
            bool: True if the password is correct, False otherwise.
        """
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        """
        Hashes a plain password using the configured scheme.

        Args:
            password (str): The plain password to hash.

        Returns:
            str: The securely hashed password.
        """
        return pwd_context.hash(password)


class TokenService:
    """
    Provides static methods for creating and validating JWT tokens.
    """
    @staticmethod
    def create_access_token(data: dict) -> str:
        """
        Creates a new JWT access token.

        Args:
            data (dict): The payload to encode in the token.

        Returns:
            str: The encoded JWT access token.
        """
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=auth_config.access_token_expire_minutes
        )
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, auth_config.secret_key, algorithm=auth_config.algorithm)

    @staticmethod
    def create_refresh_token(data: dict) -> str:
        """
        Creates a new JWT refresh token with a longer expiration.

        Args:
            data (dict): The payload to encode in the token.

        Returns:
            str: The encoded JWT refresh token.
        """
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            days=auth_config.refresh_token_expire_days
        )
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, auth_config.secret_key, algorithm=auth_config.algorithm)

    @staticmethod
    def verify_token(token: str) -> Optional[TokenPayloadDTO]:
        """
        Verifies a token's signature and expiration, returning its payload.

        Args:
            token (str): The JWT to decode.

        Returns:
            Optional[TokenPayloadDTO]: The decoded payload DTO, or None if
                validation fails.
        """
        try:
            payload = jwt.decode(
                token, auth_config.secret_key, algorithms=[auth_config.algorithm]
            )
            return TokenPayloadDTO(**payload)
        except JWTError:
            return None
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

# Initialize the password hashing context using bcrypt as the scheme.
# This context manages the hashing and verification of passwords.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class PasswordService:
    """Provides static methods for password hashing and verification.

    This class encapsulates the logic for handling user passwords securely. It uses
    the `passlib` library to ensure that passwords are not stored in plaintext.
    All methods are static, as they do not depend on the state of an instance.
    """
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verifies a plain password against its hashed version.

        This method compares a user-provided plaintext password with a stored
        hash to check for a match. It is the correct way to check if a password
        is valid without ever decrypting the stored hash.

        Args:
            plain_password (str): The password attempt from the user.
            hashed_password (str): The stored hashed password from the database.

        Returns:
            bool: True if the plain password matches the hashed password,
                False otherwise.
        """
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        """Hashes a plain password using the configured scheme.

        This method takes a plaintext password and generates a secure hash from
        it. This hash is what should be stored in the database instead of the
        password itself.

        Args:
            password (str): The plain password to hash.

        Returns:
            str: The securely hashed password.
        """
        return pwd_context.hash(password)


class TokenService:
    """Provides static methods for creating and validating JWT tokens.

    This class handles all operations related to JSON Web Tokens (JWTs), which
    are used for user authentication and authorization. It uses settings from
ax_config` to configure the secret key, algorithm, and token expiration
    times.
    """
    @staticmethod
    def create_access_token(data: dict) -> str:
        """Creates a new JWT access token.

        Access tokens are short-lived tokens that grant a user access to
        protected resources. The payload typically contains the user's
        identifier.

        Args:
            data (dict): The payload data to encode in the token (e.g.,
                {'sub': user_id}).

        Returns:
            str: The encoded JWT access token as a string.
        """
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=auth_config.access_token_expire_minutes
        )
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, auth_config.secret_key, algorithm=auth_config.algorithm)

    @staticmethod
    def create_refresh_token(data: dict) -> str:
        """Creates a new JWT refresh token with a longer expiration.

        Refresh tokens are long-lived tokens that can be used to obtain a new
        access token without requiring the user to re-authenticate.

        Args:
            data (dict): The payload data to encode in the token (e.g.,
                {'sub': user_id}).

        Returns:
            str: The encoded JWT refresh token as a string.
        """
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            days=auth_config.refresh_token_expire_days
        )
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, auth_config.secret_key, algorithm=auth_config.algorithm)

    @staticmethod
    def verify_token(token: str) -> Optional[TokenPayloadDTO]:
        """Verifies a token's signature and expiration, returning its payload.

        This method decodes a JWT, checks if its signature is valid using the
        secret key, and verifies that the token has not expired.

        Args:
            token (str): The JWT to decode and verify.

        Returns:
            Optional[TokenPayloadDTO]: The decoded payload as a `TokenPayloadDTO`
                object if the token is valid, or `None` if validation fails
                due to an invalid signature, expiration, or malformed token.
        """
        try:
            payload = jwt.decode(
                token, auth_config.secret_key, algorithms=[auth_config.algorithm]
            )
            return TokenPayloadDTO(**payload)
        except JWTError:
            return None
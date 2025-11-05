"""
Database configuration, engine setup, and session management.

This module uses pydantic-settings to manage database connection parameters
and provides a DatabaseHelper class to create an asynchronous SQLAlchemy
engine and session factory. It also defines the `ISession` dependency for
clean session injection into repositories.
"""
from sqlalchemy import exc
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from pydantic import Field, PostgresDsn
from pydantic_settings import BaseSettings
from typing import Annotated
from fastapi import Depends


class DbSettings(BaseSettings):
    """
    Defines database configuration settings loaded from environment variables.

    Attributes:
        db_url_scheme (str): The scheme for the database connection URL.
        db_host (str): The hostname of the database server.
        db_port (int): The port number of the database server.
        db_name (str): The name of the database.
        db_user (str): The username for connecting to the database.
        db_password (str): The password for the database user.
        db_echo_log (bool): If True, SQLAlchemy will log all generated SQL.
    """
    db_url_scheme: str = Field("postgresql+asyncpg", alias="DB_URL_SCHEME")
    db_host: str = Field(..., alias="DB_HOST")
    db_port: int = Field(..., alias="DB_PORT")
    db_name: str = Field(..., alias="DB_NAME")
    db_user: str = Field(..., alias="DB_USER")
    db_password: str = Field(..., alias="DB_PASSWORD")
    db_echo_log: bool = Field(False, alias="DB_ECHO_LOG")

    @property
    def database_url(self) -> str:
        """Constructs the full database connection URL."""
        return (
            f"{self.db_url_scheme}://{self.db_user}:{self.db_password}@"
            f"{self.db_host}:{self.db_port}/{self.db_name}"
        )

settings = DbSettings()


class DatabaseHelper:
    """
    Manages the asynchronous database engine and session creation.

    Args:
        url (str): The full database connection URL.
        echo (bool): Whether to enable SQL query logging.
    """
    def __init__(self, url: str, echo: bool = False):
        self.engine = create_async_engine(url=url, echo=echo)
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False
        )

    async def get_session(self):
        """
        Provides a new database session for a single request.

        This generator function is used as a FastAPI dependency to ensure that
        a session is created for each request and properly closed afterward,
        with transaction rollback on error.

        Yields:
            AsyncSession: The SQLAlchemy asynchronous session.
        """
        session: AsyncSession = self.session_factory()
        try:
            yield session
        except exc.SQLAlchemyError:
            await session.rollback()
            raise
        finally:
            await session.close()

db_helper = DatabaseHelper(settings.database_url, settings.db_echo_log)

ISession: type[AsyncSession] = Annotated[AsyncSession, Depends(db_helper.get_session)]
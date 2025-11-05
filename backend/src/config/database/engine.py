"""Database engine and session management."""
from asyncio import current_task
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    async_scoped_session,
    create_async_engine,
)
from src.config.database.settings import settings

class DatabaseHelper:
    """
    A class for managing database connections and sessions.

    Args:
        url (str): The URL for the database connection.
        echo (bool): Whether to enable echo logging for the engine.
    """
    def __init__(self, url: str, echo: bool = False):
        self.engine = create_async_engine(url=url, echo=echo)
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    def get_scoped_session(self):
        """Returns a scoped session for the current task."""
        return async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task,
        )

    @asynccontextmanager
    async def get_db_session(self):
        """
        Provides a database session within an asynchronous context manager.

        Yields:
            AsyncSession: The database session.
        """
        from sqlalchemy import exc

        session: AsyncSession = self.session_factory()
        try:
            yield session
        except exc.SQLAlchemyError:
            await session.rollback()
            raise
        finally:
            await session.close()

    async def get_session(self):
        """
        Generator that provides a database session.

        Yields:
            AsyncSession: The database session.
        """
        from sqlalchemy import exc

        session: AsyncSession = self.session_factory()
        try:
            yield session
        except exc.SQLAlchemyError:
            await session.rollback()
            raise
        finally:
            await session.close()

db_helper = DatabaseHelper(settings.database_url, settings.db_echo_log)
"""
Defines fixtures for the Pytest testing suite.

This file configures the test environment, including creating an isolated
in-memory SQLite database for each test session and providing a test client
for making API requests.
"""
import asyncio
from typing import AsyncGenerator

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app import get_app
from backend.config.database import db_helper, DatabaseHelper
from backend.libs.base_model import Base


# Create a new test app instance
app = get_app()

@pytest.fixture(scope="session")
def event_loop():
    """
    Creates an instance of the default asyncio event loop for the test session.
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def test_db_engine():
    """
    Creates a new database engine for the test session.

    This uses an in-memory SQLite database to ensure tests are fast and isolated.
    """
    # Use in-memory SQLite for testing
    test_db_url = "sqlite+aiosqlite:///:memory:"
    test_db_helper = DatabaseHelper(url=test_db_url, echo=False)
    yield test_db_helper.engine
    await test_db_helper.engine.dispose()


@pytest.fixture(scope="function", autouse=True)
async def setup_database(test_db_engine):
    """
    A fixture that creates all database tables before each test and drops
    them after, ensuring a clean state for every test function.
    """
    async with test_db_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_db_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function")
async def client(test_db_engine) -> AsyncGenerator[AsyncClient, None]:
    """
    Provides an authenticated test client for making API requests.

    This fixture overrides the main database dependency with the isolated
    test database session.
    """
    async def override_get_session():
        """Dependency override for providing a test database session."""
        async with test_db_engine.connect() as connection:
            async with connection.begin() as transaction:
                async_session = AsyncSession(bind=connection)
                yield async_session
                await transaction.rollback()

    app.dependency_overrides[db_helper.get_session] = override_get_session

    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()
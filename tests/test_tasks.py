"""
Integration tests for the Task API endpoints.
"""
import pytest
from httpx import AsyncClient

# Mark all tests in this module to be run with asyncio
pytestmark = pytest.mark.asyncio


class TestTaskAPI:
    """A test class to group all task-related API tests."""

    @pytest.fixture(scope="class")
    async def authenticated_client(self, client: AsyncClient) -> AsyncClient:
        """
        A fixture that provides a client pre-authenticated with a test user.
        """
        # Register a new user
        await client.post(
            "/api/auth/register",
            json={"username": "testuser", "email": "test@example.com", "password": "password123"},
        )
        # Log in to get tokens
        response = await client.post(
            "/api/auth/login",
            json={"username": "testuser", "password": "password123"},
        )
        token = response.json()["access_token"]
        # Set the auth header for all subsequent requests with this client
        client.headers["Authorization"] = f"Bearer {token}"
        return client

    async def test_create_task(self, authenticated_client: AsyncClient):
        """
        Test Case 1: Create a new task.

        Verifies that a logged-in user can successfully create a new task
        and that the API returns the correct data with a 201 status code.
        """
        response = await authenticated_client.post(
            "/api/tasks/",
            json={"title": "My First Test Task", "description": "This is a test."},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "My First Test Task"
        assert data["description"] == "This is a test."
        assert data["status"] == "pending"
        assert "id" in data

    async def test_get_tasks(self, authenticated_client: AsyncClient):
        """
        Test Case 2: Get a list of tasks.

        Verifies that a user can retrieve their own tasks. This test first
        creates a task to ensure the list is not empty.
        """
        # First, create a task to ensure there is something to fetch
        await authenticated_client.post(
            "/api/tasks/",
            json={"title": "Task to be fetched", "description": "Fetch me."},
        )

        # Now, get the list of tasks
        response = await authenticated_client.get("/api/tasks/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["title"] == "Task to be fetched"

    async def test_unauthenticated_access(self, client: AsyncClient):
        """
        Test Case 3: Deny access to unauthenticated users.

        Verifies that attempting to access a protected endpoint without a
        valid token results in a 401 Unauthorized error.
        """
        response = await client.get("/api/tasks/")
        assert response.status_code == 401
        assert response.json()["detail"] == "Not authenticated"
# Full-Stack Task Management API

This is a production-ready, full-stack application built for a technical evaluation for a Full-Stack Developer position. The project features a robust RESTful API backend powered by **FastAPI** and a modern, responsive Single-Page Application (SPA) frontend built with **React**.

The entire application is containerized with **Docker** and orchestrated with **Docker Compose**, following a clean, layered architecture and adhering to modern software development best practices.

## Core Features

### Backend (FastAPI)
-   **Clean Layered Architecture:** Follows a strict Router -> Service -> Repository pattern for maximum separation of concerns and testability.
-   **Secure JWT Authentication:** Complete token-based security with short-lived access tokens and long-lived refresh tokens.
-   **Automatic Token Refresh:** Implements refresh token rotation, providing a seamless and secure user experience.
-   **Full CRUD for Tasks:** All required operations for creating, reading, updating, and deleting tasks.
-   **Task Filtering:** Ability to filter the task list by status (`pending`, `in_progress`, `done`).
-   **Database Migrations:** Uses **Alembic** to manage database schema changes, with migrations applied automatically on startup.
-   **Dependency Injection:** Heavily utilizes FastAPI's dependency injection system for clean, decoupled code.
-   **Automatic API Documentation:** Provides interactive Swagger UI and ReDoc documentation out of the box.

### Frontend (React)
-   **Modern React Stack:** Built with functional components, Hooks, and the Context API.
-   **Component-Based Architecture:** Clear separation of concerns into pages, components, services, and hooks.
-   **Global State Management:** Uses React Context for managing global authentication state.
-   **Protected Routes:** Client-side routing that protects the main dashboard from unauthenticated access.
-   **Full Task Management UI:** A clean interface for adding, viewing, updating, and deleting tasks.
-   **Task Filtering UI:** Allows users to filter their task list by status.
-   **Responsive Design:** Styled with **TailwindCSS** for a responsive layout that works on screens from 320px to 1440px and beyond.

## Tech Stack

| Category       | Technology                                                                            |
|----------------|---------------------------------------------------------------------------------------|
| **Backend**    | Python 3.12, FastAPI, Uvicorn, SQLAlchemy 2.0 (Async), Pydantic, Passlib, python-jose |
| **Frontend**   | React 18, React Router, Axios, TailwindCSS, jwt-decode                                |
| **Database**   | PostgreSQL                                                                            |
| **Migrations** | Alembic                                                                               |
| **Testing**    | Pytest, Pytest-Asyncio, HTTPX                                                         |
| **Deployment** | Docker, Docker Compose, Nginx (as a reverse proxy)                                    |
| **Tooling**    | `nvm`, `venv`, `pip`, `npm`, `pyproject.toml`                                         |

## Architectural Overview

The backend follows a clean, decoupled, 3-tier architecture to ensure maintainability and scalability.

1.  **Router Layer (`/router.py`):** Defines the API endpoints. It is responsible for handling HTTP requests and responses, validating data with Pydantic DTOs, and delegating all business logic to the service layer. It contains no business logic itself.
2.  **Service Layer (`/service.py`):** Contains all the business logic. It orchestrates operations, enforces rules (like ownership checks), and coordinates between different repositories. It never interacts with the database directly.
3.  **Repository Layer (`/repository.py`):** The data access layer. This is the only part of the application that directly interacts with the database via SQLAlchemy. It performs all CRUD operations and returns DTOs to the service layer.

This strict separation ensures that each part of the application has a single responsibility, making the codebase easy to test, debug, and extend.

## Getting Started (Docker - Recommended)

The easiest and most reliable way to run the entire full-stack application is with Docker Compose.

### Prerequisites
-   Docker
-   Docker Compose

### 1. Clone the Repository
```bash
git clone https://github.com/fluffy-dev/FocalOfAttention-TestWork.git
cd FocalOfAttention-TestWork
```

### 2. Configure Environment Variables
Create a `.env` file in the project root by copying the example. No changes are needed for the default Docker setup.
```bash
cp .env.example .env
```

### 3. Build and Run the Application
Execute the following command from the project root. This will build the images for the backend and frontend, start all services, and automatically run the database migrations.
```bash
docker-compose up --build
```

### 4. Access the Application
-   **Frontend Application:** Open your browser and navigate to `http://localhost:3000`
-   **Backend API Docs:** The API documentation is available at `http://localhost:3000/docs` (served through the Nginx reverse proxy).

The application is now fully running.

---

## Local Development (Without Docker)
<details>
<summary>Click to expand for local development instructions</summary>

### Prerequisites
-   Python 3.12+ and a virtual environment tool (e.g., `venv`).
-   Node.js 20+ and a version manager (e.g., `nvm`).
-   A running PostgreSQL instance.

### Backend Setup
1.  **Navigate to the project root.**
2.  **Create and activate a Python virtual environment:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```
3.  **Install dependencies and the project in editable mode:**
    ```bash
    pip install -r test-requirements.txt
    ```
4.  **Configure `.env`:** Update the `DB_HOST` to `localhost` and ensure your database credentials match your local PostgreSQL setup.
5.  **Run migrations:**
    ```bash
    alembic upgrade head
    ```
6.  **Start the backend server:**
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```
The backend will be running on `http://localhost:8000`.

### Frontend Setup
1.  **Navigate to the `frontend` directory:**
    ```bash
    cd frontend
    ```
2.  **Use the correct Node.js version (if you have `.nvmrc`):**
    ```bash
    nvm use
    ```
3.  **Install dependencies:**
    ```bash
    npm install
    ```
4.  **Configure `.env`:** Ensure `REACT_APP_API_BASE_URL` is set to `http://localhost:8000/api`.
5.  **Start the frontend server:**
    ```bash
    npm start
    ```
The frontend will be running on `http://localhost:3000`.

</details>

---

## Running the Test Suite

The backend includes a comprehensive test suite using Pytest.

### Prerequisites
-   All development dependencies must be installed (`pip install -e ".[test]"`).

### Run Command
From the **project root directory**, execute:
```bash
pytest -v
```
The tests will run against a clean, in-memory SQLite database to ensure they do not affect your development data.

## API Endpoints Overview

The API is structured logically by resource. All endpoints under `/api/` are protected unless otherwise noted.

-   **Authentication (`/api/auth`)**
    -   `POST /register`: Create a new user and return tokens. (Public)
    -   `POST /login`: Log in and return tokens. (Public)
    -   `POST /refresh`: Get a new set of tokens using a refresh token.

-   **Tasks (`/api/tasks`)**
    -   `POST /`: Create a new task.
    -   `GET /`: Get all tasks for the logged-in user.
    -   `GET /{task_id}`: Get a specific task by ID.
    -   `PUT /{task_id}`: Update a task.
    -   `DELETE /{task_id}`: Delete a task.

## Project Structure

```
.
├── backend/
│   ├── app.py             # FastAPI App Factory
│   ├── config/            # Configuration modules
│   ├── libs/              # Shared libraries (Base Model, Exceptions)
│   ├── auth/              # Registration & Login logic
│   ├── user/              # User CRUD logic
│   ├── task/              # Task CRUD logic
│   └── security/          # JWT services & dependencies
├── frontend/
│   ├── src/
│   │   ├── components/    # Reusable UI components
│   │   ├── context/       # React Context for global state
│   │   ├── hooks/         # Custom React hooks
│   │   ├── pages/         # Page-level components
│   │   └── services/      # API communication layer
│   ├── Dockerfile         # Frontend Docker build
│   └── nginx.conf         # Nginx reverse proxy config
├── tests/
│   ├── conftest.py        # Pytest fixtures and test setup
│   └── test_tasks.py      # Task API integration tests
├── alembic/                # Alembic migration scripts
├── .env.example           # Example environment variables
├── docker-compose.yml     # Docker Compose orchestration
├── Dockerfile             # Backend Docker build
├── pyproject.toml         # Python project definition
└── README.md              # This file
```


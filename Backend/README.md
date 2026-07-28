# SkillBranch Backend

## About the Backend

SkillBranch is a web-based skill and progress tracking application. This backend
provides the API used to create an account and organize learning in a structured
hierarchy:

```text
User
└── Skill
    └── Project
        └── Task
```

Users can track skills, group practical projects under each skill, create tasks
with deadlines, and mark those tasks as completed. Every skill, project, and task
request is scoped to the authenticated user, preventing users from accessing one
another's data.

## Tech Stack

- **Python 3.12+** — backend programming language
- **FastAPI** — API framework, routing, dependency injection, validation, and
  interactive API documentation
- **Uvicorn** — ASGI development server
- **SQLAlchemy 2.0** — ORM, database sessions, relationships, and queries
- **SQLite** — local relational database
- **Pydantic** and **pydantic-settings** — request validation and environment
  configuration
- **PyJWT** — JSON Web Token creation and validation
- **pwdlib with Argon2** — secure password hashing and verification
- **OAuth2 password bearer flow** — protected endpoint authentication
- **python-multipart** — form-data support for login requests
- **CORS middleware** — frontend-to-backend communication during development
- **pytest** and **HTTPX/TestClient** — automated endpoint and authentication
  testing
- **Ruff** and **Pyright** — linting and type checking
- **uv** — dependency and virtual-environment management

## API Methods

The API runs at `http://localhost:8000` by default. FastAPI also generates
interactive documentation at:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

All endpoints except signup and login require an access token:

```http
Authorization: Bearer <access_token>
```

### User Methods

| Method | Endpoint | Description | Request data |
| --- | --- | --- | --- |
| `POST` | `/user/signup` | Creates a user and returns a bearer token. | JSON: `username`, `email`, `password` |
| `POST` | `/user/login` | Verifies an existing user and returns a bearer token. | Form data: `username` (email), `password` |

Passwords must contain between 8 and 200 characters. Email addresses are
normalized to lowercase before storage and lookup.

### Skill Methods

| Method | Endpoint | Description | Request data |
| --- | --- | --- | --- |
| `GET` | `/skill/skills` | Returns all skills owned by the authenticated user. | Optional query: `offset`, `limit` |
| `GET` | `/skill/skill/{skill_id}` | Returns one owned skill. | UUID path parameter |
| `POST` | `/skill/create_skill` | Creates a skill for the authenticated user. | JSON: `name`, `description` |
| `PUT` | `/skill/update_skill` | Updates an owned skill. | JSON: `id`, `name`, `description` |
| `DELETE` | `/skill/delete_skill` | Deletes a skill and its related projects and tasks. | JSON: `id` |

Skill names must be unique for each user.

### Project Methods

| Method | Endpoint | Description | Request data |
| --- | --- | --- | --- |
| `GET` | `/project/projects/{skill_id}` | Returns all projects under an owned skill. | UUID path parameter; optional query: `offset`, `limit` |
| `GET` | `/project/project/{skill_id}/{project_id}` | Returns one project under an owned skill. | UUID path parameters |
| `POST` | `/project/create_project` | Creates a project under an owned skill. | JSON: `skill_id`, `project_name`, `description` |
| `PUT` | `/project/update_project` | Updates an owned project. | JSON: `skill_id`, `project_id`, `project_name`, `description` |
| `DELETE` | `/project/delete_project` | Deletes a project and its related tasks. | JSON: `skill_id`, `project_id` |

Project names must be unique within each skill.

### Task Methods

| Method | Endpoint | Description | Request data |
| --- | --- | --- | --- |
| `GET` | `/task/tasks/{skill_id}/{project_id}` | Returns all tasks under an owned project. | UUID path parameters; optional query: `offset`, `limit` |
| `GET` | `/task/task/{skill_id}/{project_id}/{task_id}` | Returns one task under an owned project. | UUID path parameters |
| `POST` | `/task/create_task` | Creates a task under an owned project. | JSON: `skill_id`, `project_id`, `task_name`, `description`, `deadline` |
| `PUT` | `/task/update_task` | Updates an owned task. | JSON: `skill_id`, `project_id`, `task_id`, `task_name`, `description`, `deadline` |
| `DELETE` | `/task/delete_task` | Deletes an owned task. | JSON: `skill_id`, `project_id`, `task_id` |
| `PATCH` | `/task/toggle_task` | Sets a task's completion state. | JSON: `skill_id`, `project_id`, `task_id`, `toggle` |
| `GET` | `/task/near_deadline_tasks` | Returns incomplete tasks ordered by the nearest deadline. | None |

Task names must be unique within each project. The `deadline` field accepts an
ISO 8601 date-time value, and `toggle` is a boolean.

## Data Model

- A **User** can own many skills.
- A **Skill** belongs to one user and can contain many projects.
- A **Project** belongs to one skill and can contain many tasks.
- A **Task** belongs to one project and stores its deadline and completion state.
- UUIDs are used as primary keys.
- Deleting a parent resource cascades to its child resources.

## Authentication and Security

- Passwords are hashed with the recommended `pwdlib` Argon2 configuration and
  are never stored as plain text.
- Successful signup and login requests return a JWT bearer token.
- Tokens store the user's email in the `sub` claim and use a configurable
  expiration period.
- Protected database queries include the authenticated user's ID, keeping each
  user's resources isolated.

## Local Development

### 1. Install dependencies

Install [uv](https://docs.astral.sh/uv/) if it is not already available, then
run:

```bash
uv sync
```

### 2. Configure the environment

Create a `.env` file in the backend directory:

```env
DATABASE_URL=sqlite:///./database/skillbranch.db
JWT_SECRET_KEY=replace-with-a-long-random-secret
EXPIRATION_MINUTE=15
EXPIRATION_HOUR=0
EXPIRATION_DAY=0
ALGORITHM=HS256
```

Ensure that the `database` directory exists before starting the application.
Do not commit the `.env` file or expose the JWT secret.

### 3. Start the server

Using the FastAPI development command:

```bash
uv run fastapi dev
```

Alternatively, use the project entry point:

```bash
uv run python main.py
```

The server will be available at `http://localhost:8000`. The current CORS
configuration allows the frontend development origin
`http://127.0.0.1:5500`.

## Testing and Code Quality

Run the automated tests:

```bash
uv run pytest
```

Run linting and type checking:

```bash
uv run ruff check .
uv run pyright
```

The test suite covers user signup and login, JWT rejection and expiration,
normal CRUD workflows, malformed and nonexistent IDs, cascading deletion, and
cross-user access protection.

## Developer's Note

This project was built as a full-stack learning experience, covering both
frontend and backend development. I learned a great deal while connecting the
user interface, API, authentication, and database layers. The frontend is still
rough around the edges, but it has helped me identify the design and
architecture improvements I want to carry into upcoming projects.

# Task Manager API

A RESTful Task Manager API built with **Django** and **Django REST Framework**. Supports full CRUD operations on tasks, JWT authentication, role-based access control, filtering, pagination, and interactive Swagger documentation.

---

## Tech Stack

- **Django 4.2** + **Django REST Framework 3.15**
- **djangorestframework-simplejwt** — JWT authentication
- **drf-yasg** — Swagger + ReDoc docs
- **django-filter** — Query-param filtering
- **SQLite** (dev) — swappable for PostgreSQL in production
- **pytest + pytest-django** — unit tests

---

## Project Structure

```
r-ztm-f-d/
├── task_manager/        # Django project (settings, urls)
├── apps/
│   ├── users/           # Auth app (User model, register, login)
│   └── tasks/           # Tasks app (Task model, CRUD, permissions)
├── tests/               # pytest test suite
├── requirements.txt
├── pytest.ini
└── .env.example
```

---

## Setup & Run

### 1. Clone and install dependencies

```bash
git clone <repo-url>
cd r-ztm-f-d
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
# Edit .env and set a strong SECRET_KEY
```

### 3. Apply database migrations

```bash
python3 manage.py migrate
```

### 4. (Optional) Create an admin user

```bash
python3 manage.py createsuperuser
```

### 5. Run the development server

```bash
python3 manage.py runserver
```

The API will be available at `http://localhost:8000/`.

---

## API Documentation

Once the server is running, visit:

| URL | Description |
|-----|-------------|
| `http://localhost:8000/api/docs/` | Swagger UI — try all endpoints interactively |
| `http://localhost:8000/api/redoc/` | ReDoc — clean reference documentation |
| `http://localhost:8000/admin/` | Django admin panel |

---

## API Endpoints

### Authentication

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/api/auth/register/` | None | Register a new user |
| POST | `/api/auth/login/` | None | Login, returns JWT tokens |
| GET | `/api/auth/users/` | Admin only | List all registered users |

**Register request:**
```json
{
  "username": "john",
  "email": "john@example.com",
  "password": "securepass123"
}
```

**Login request:**
```json
{
  "email": "john@example.com",
  "password": "securepass123"
}
```

**Login response:**
```json
{
  "access": "<JWT access token>",
  "refresh": "<JWT refresh token>",
  "user": { "id": 1, "username": "john", "email": "john@example.com", "role": "user" }
}
```

Use the `access` token in the `Authorization` header for all protected requests:
```
Authorization: Bearer <access token>
```

---

### Tasks

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/api/tasks/` | Required | List tasks (paginated, filterable) |
| POST | `/api/tasks/` | Required | Create a new task |
| GET | `/api/tasks/<id>/` | Required | Retrieve a single task |
| PUT | `/api/tasks/<id>/` | Owner / Admin | Fully update a task |
| PATCH | `/api/tasks/<id>/` | Owner / Admin | Partially update a task |
| DELETE | `/api/tasks/<id>/` | Owner / Admin | Delete a task |

**Create task request:**
```json
{
  "title": "Write API docs",
  "description": "Document all endpoints",
  "completed": false
}
```

**Task response:**
```json
{
  "id": 1,
  "title": "Write API docs",
  "description": "Document all endpoints",
  "completed": false,
  "created_at": "2026-02-26T10:30:00Z",
  "updated_at": "2026-02-26T10:30:00Z",
  "owner": "john@example.com"
}
```

---

### Filtering & Pagination

| Query Param | Example | Description |
|-------------|---------|-------------|
| `completed` | `?completed=true` | Filter by completion status |
| `search` | `?search=report` | Search title & description |
| `page` | `?page=2` | Page number |
| `page_size` | `?page_size=5` | Results per page (default: 10) |
| `ordering` | `?ordering=-created_at` | Sort by field |

**Paginated response:**
```json
{
  "count": 25,
  "next": "http://localhost:8000/api/tasks/?page=3",
  "previous": "http://localhost:8000/api/tasks/?page=1",
  "results": [ ... ]
}
```

---

## User Roles

| Role | Permissions |
|------|-------------|
| `user` (default) | Create tasks; read, update, delete **own** tasks only |
| `admin` | Full access to **all** tasks; promotes via Django admin |

To promote a user to admin: open Django admin → Users → set role to `admin`.

---

## Running Tests

```bash
pytest tests/ -v
```

**Test coverage (25 tests):**
- Auth: register (success, duplicate email, short password), login (success, wrong password, nonexistent user)
- Tasks: create, list, retrieve, update, delete
- Access control: unauthenticated → 401, non-owner → 403/404
- Filtering: `?completed=true/false`
- Pagination: response structure, `?page_size` param
- Admin tasks: sees all tasks, can delete any task
- Roles: admin can list users, regular user gets 403, unauthenticated gets 401

# FastAPI Task Manager API

A simple Task Manager REST API built with FastAPI, JWT authentication, and async SQLAlchemy.

## Features

* User registration
* JWT authentication
* Create, read, update, and delete tasks
* User-specific task ownership
* Async SQLAlchemy support
* Pydantic validation
* Automatic database table creation

---

# Tech Stack

* FastAPI
* SQLAlchemy (Async)
* PostgreSQL
* JWT Authentication
* Pydantic v2
* Uvicorn

---

# Installation

## Clone repository

```bash
git clone https://github.com/deamanda/fastapi_tasks.git
cd fastapi_tasks
```

---

## Create virtual environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

# Install dependencies

```bash
pip install -r requirements.txt
```

---

# Run the server

```bash
fastapi dev
```

Server will start at:

```text
http://127.0.0.1:8000
```

---

# Interactive API Docs

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

ReDoc:

```text
http://127.0.0.1:8000/redoc
```

---

# Authentication

The API uses JWT Bearer authentication.

## Login

```http
POST /auth/login
```

### Form Data

| Field    | Type   |
| -------- | ------ |
| username | string |
| password | string |

### Response

```json
{
  "access_token": "your_token",
  "token_type": "Bearer"
}
```

Use the token in Swagger Authorize button:

```text
Bearer <token>
```

---

# API Endpoints

## Users

### Create User

```http
POST /users/
```

### Get Current User

```http
GET /users/me/
```

---

## Tasks

### Get All Tasks

```http
GET /tasks/
```

### Get Task By ID

```http
GET /tasks/{task_id}
```

### Create Task

```http
POST /tasks/
```

### Update Task

```http
PUT /tasks/{task_id}
```

### Delete Task

```http
DELETE /tasks/{task_id}
```

---

# Example Task Payload

```json
{
  "title": "Learn FastAPI",
  "description": "Study authentication and async SQLAlchemy",
  "priority": 1,
  "due_date": "2026-05-25",
  "completed": false
}
```

---

# Environment Variables

Create a `.env` file:

```env
DB_HOST=database_host
DB_PORT=database_port
POSTGRES_DB=database_name
POSTGRES_USER=postgres_user
POSTGRES_PASSWORD=postgres_password
SECRET_KEY=your_secret_key
ALGORITHM=password_hashing_algorithm
ACCESS_TOKEN_EXPIRE_MINUTES=access_token_expire_minutes
```

---

# Database

Tables are automatically created on application startup.

---

# Error Handling

The API returns standard HTTP status codes:

| Code | Description              |
| ---- | ------------------------ |
| 200  | Success                  |
| 204  | Resource deleted         |
| 401  | Unauthorized             |
| 404  | Resource not found       |
| 409  | Duplicate username/email |

---

# License

This project is licensed under the MIT License.

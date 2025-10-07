# NEXTstep Server

A FastAPI backend for user management and AI‑assisted scholarship matching. Users can register, upload a CV (PDF), have it parsed into structured data, and receive ranked scholarship matches using a SentenceTransformer model. The service also supports basic profile management, skills, and static profile image hosting.

---

## Key Features

- FastAPI application with modular routers
  - Auth (registration, login via OAuth2 password flow)
  - Users (profile, password change, skills, CV upload/update)
  - Scholarship (CRUD-lite: list, get, create; plus matching endpoints)
- Async PostgreSQL via SQLAlchemy 2.x + asyncpg
- Alembic migrations for schema management
- AI matching engine using SentenceTransformer (all-MiniLM-L6-v2)
- CV parsing with pdfplumber + spaCy (en_core_web_sm)
- Background tasks for recalculating matches
- Centralized exception handling
- Simple rate-limiting on sensitive endpoints (registration)
- Static files (profile images) served under `/api/v1/static`

---

## Architecture Overview

- Entry point: `src/main.py`
  - Configures logging and CORS
  - Sets FastAPI lifespan to initialize the matching model
  - Mounts static files at `/api/v1/static` (backed by `public/images`)
  - Registers routers and exception handlers
- Routers: `src/api.py`
  - `/api/v1/auth` → `src/auth/controllers.py`
  - `/api/v1/users` → `src/users/controllers.py`
  - `/api/v1/scholarship` → `src/scholarship/controllers.py`
- Database layer: `src/database/core.py`
  - Async engine + session factory
  - `Base = declarative_base()` for SQLAlchemy models
  - Reads DB connection details from environment variables
- Entities (ORM models): `src/entities/*.py`
  - `User`, `Skill`, `UserSkill` (many-to-many), `Cv`, `Scholarship`, `ScholarshipMatch`
- Migrations: `alembic/` (autogenerate against `Base.metadata`)
- Matching (AI): `src/ai_models/model.py`
  - Loads SentenceTransformer `all-MiniLM-L6-v2`
  - Computes a similarity score from CV text → scholarship requirements/description
- CV processing: `src/utils/cv_parser.py`, `src/utils/cv_statement.py`
  - Extracts fields from a PDF CV (skills, education, GPA, etc.)
  - Converts a stored CV into a human-readable statement used by the matcher
- Background tasks: `src/background_tasks/tasks.py`
  - Batch matching for a new scholarship against users
  - Recompute matches for a user across scholarships
- Exception handling: `src/exceptions/*`
  - Consistent JSON error responses and validation errors
- Rate limiting: `src/rate_limiting.py` + decorator usage in auth controller
- Optional Socket.IO: `src/sio/event_handlers.py` (not wired by default)

---

## Tech Stack

- Python, FastAPI, Starlette
- SQLAlchemy 2.x (async), asyncpg
- Alembic
- SentenceTransformers, spaCy, pdfplumber
- Uvicorn (dev server)

---

## Getting Started

### Prerequisites

- Python 3.11+ recommended (project developed with modern FastAPI/SQLAlchemy)
- PostgreSQL running locally
- PowerShell on Windows (commands below use PowerShell syntax)

### Clone and set up environment

```powershell
# (optional) create and activate a virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# install dependencies
pip install -r requirements.txt

# additional runtime models/packages used by the app
pip install sentence-transformers
python -m spacy download en_core_web_sm
```

### Configure environment variables

Create a `.env` file in the repository root with at least:

```dotenv
# Database
DB_USERNAME=postgres
DB_PASSWORD=postgres
DB_PORT=5432
DB_NAME=nextstep_db

# Auth/JWT
SECRET_KEY=replace-with-a-strong-secret
ALGORITHM=HS256
TOKEN_EXP_MIN=60
```

`src/database/core.py` reads these variables to construct the async database URL. Alembic also needs a connection URL; adjust `alembic.ini`'s `sqlalchemy.url` to point to the same database if you plan to run migrations from Alembic CLI.

### Database migrations

If starting fresh, generate and/or apply migrations via Alembic:

```powershell
# make sure alembic.ini has the correct sqlalchemy.url
# then apply the latest migrations
alembic upgrade head

# (optional) autogenerate a new migration if you change models
# alembic revision --autogenerate -m "describe change"
# alembic upgrade head
```

The repository already includes multiple revisions in `alembic/versions/` that define users, skills, scholarships, CVs, and scholarship matches.

### Run the server (development)

```powershell
# Option 1: uvicorn
uvicorn src.main:app --reload --port 8000

# Option 2: fastapi CLI (installed via requirements)
# fastapi dev src/main.py --port 8000
```

- API docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Static images: http://localhost:8000/api/v1/static

---

## API Overview

Base prefix for routers: `/api/v1`

### Auth (`/auth`)

- POST `/auth/register` (multipart/form-data)
  - Body (form fields): `firstname`, `lastname`, `username`, `email`, `password`, `role` (optional; `user` by default)
  - File: `profile_image` (optional)
  - Rate limited via `slowapi`
- POST `/auth/token`
  - OAuth2 Password flow; returns `{ access_token, token_type }`
  - Use in subsequent requests: `Authorization: Bearer <token>`

### Users (`/users`)

- GET `/users/me`
  - Returns current user with optional `cv` field
- PATCH `/users/me`
  - Form body: any of `firstname`, `lastname`, `username`, `email`
- POST `/users/me/change-password`
  - Form body: `old_password`, `new_password`, `confirm_password`
- PATCH `/users/me/detail`
  - Form body: `skills` as a list of strings (may be empty to clear)
- PATCH `/users/me/cv`
  - JSON body of CV fields (all optional): `skills` (JSON string), `university`, `degree`, `major`, `graduation_year`, `gpa`, `nationality`, `gender`, `date_of_birth`
- POST `/users/me/upload-cv`
  - Upload a PDF CV file under field name `cv`
  - The file is parsed; extracted values stored in `cv` table

### Scholarship (`/scholarship`)

- GET `/scholarship?limit=10&offset=0`
  - Returns paginated list; query params validated via `src/shared/model.Parameters`
- POST `/scholarship`
  - JSON body: `name`, `description`, `requirements`, `is_fully_funded`, optional `study_level`, `field_of_study`, `eligible_nationalities`, `country`
  - Triggers background task to match the new scholarship against existing users
- GET `/scholarship/matched-scholarships`
  - Returns sorted matches for current user (highest score first)
- POST `/scholarship/rematch`
  - Recomputes matches for the current user across all scholarships
- GET `/scholarship/{id}`
  - Returns one scholarship by UUID

---

## Data Model (simplified)

- `User` (one-to-many `ScholarshipMatch`, one-to-one `Cv`, many-to-many `Skill` via `UserSkill`)
- `Cv` (text fields about education, GPA, skills, etc.)
- `Scholarship` (name, description, requirements, category fields)
- `ScholarshipMatch` (user_id, scholarship_id, match_percent float)

Alembic revisions under `alembic/versions/` define and evolve these tables.

---

## Matching Pipeline

1. CV text is parsed from PDF via `pdfplumber` and processed with spaCy to extract:
   - skills, university, degree, major, graduation_year, gpa, nationality, gender, date_of_birth
2. `CvToStatement` formats stored CV data into a concise profile statement.
3. `AsymmetricScholarshipMatcher` embeds the CV statement and scholarship text
   (`description` + `requirements` + relevant fields) with `all-MiniLM-L6-v2` and computes cosine similarity.
4. Matches are stored in `scholarship_matchs` and exposed in sorted order.

---

## Configuration Notes

- CORS: `src/setting/__init__.py` currently allows all origins (`origins = ["*"]`). For production, restrict this list.
- Static files: profile images saved to `public/images`, accessible at `/api/v1/static`.
- JWT: configured via `SECRET_KEY`, `ALGORITHM`, and `TOKEN_EXP_MIN` in `.env`.
- Alembic: update `alembic.ini` `sqlalchemy.url` to match your environment for migrations.

---

## Troubleshooting

- SentenceTransformers not found: install `sentence-transformers` (not pinned in `requirements.txt`).
- spaCy model missing: run `python -m spacy download en_core_web_sm`.
- Database connection errors: ensure `.env` is loaded and Postgres is reachable; verify `DB_*` vars.
- File upload errors: CV uploads must be PDFs; the service enforces a size check.
- Rate limiting: If you hit a 429 on `/auth/register`, wait and retry later.

---

## Project Structure

```
nextstep-server/
├─ alembic/                 # Alembic configuration and migration scripts
├─ public/
│  └─ images/               # Uploaded profile images (served at /api/v1/static)
├─ src/
│  ├─ ai_models/            # SentenceTransformer-based matcher
│  ├─ auth/                 # OAuth2, registration, login
│  ├─ background_tasks/     # Match recalculation tasks
│  ├─ database/             # SQLAlchemy async engine/session and Base
│  ├─ dependencies/         # App lifespan + DI for matcher model
│  ├─ entities/             # SQLAlchemy ORM models
│  ├─ exceptions/           # Centralized exception definitions/handlers
│  ├─ scholarship/          # Endpoints and services for scholarships
│  ├─ shared/               # Common models/enums
│  ├─ sio/                  # Socket.IO handlers (not mounted by default)
│  ├─ users/                # Endpoints and services for users
│  ├─ utils/                # CV parsing and statement generation
│  ├─ api.py                # Router registration
│  ├─ main.py               # FastAPI app factory + CORS + static + exceptions
│  └─ logging.py            # Log level configuration
├─ requirements.txt         # Python dependencies
└─ alembic.ini              # Alembic configuration
```

---

---

## Acknowledgements

- FastAPI & Starlette
- SQLAlchemy & Alembic
- SentenceTransformers
- spaCy & pdfplumber

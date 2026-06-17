# ORM Module

This repository contains a SQLAlchemy ORM-based database model for a college system and Alembic migration support.

## Structure

- `models.py` - SQLAlchemy model definitions and database engine setup.
- `crud.py` - example session usage, sample inserts, queries, and updates.
- `alembic.ini` - Alembic configuration for migrations.
- `migrations/` - Alembic migration environment and version history.
- `migrations/env.py` - migration environment setup using `Base.metadata` from `models.py`.

## Models

The ORM defines the following entities:

- `Department` - holds department metadata and relationships to `Student`, `Course`, and `Professor`.
- `Student` - stores student details, enrollment year, active status, and department link.
- `Course` - stores course metadata and its department.
- `Enrollment` - links students and courses and includes enrollment date and grade.

## Requirements

- Python 3.8+
- `SQLAlchemy`
- `alembic`
- `mysql-connector-python`

Install dependencies with:

```bash
pip install sqlalchemy alembic mysql-connector-python
```

## Database Configuration

This module now uses a `.env` file at the repository root to store database connection settings.

Example `.env` values:

```env
DB_DRIVER=mysql+mysqlconnector
DB_USER=root
DB_PASSWORD=<your_password_here>
DB_HOST=localhost
DB_NAME=college_db_orm
DB_ECHO=True
```

Optionally, you can also provide a single connection string via `DATABASE_URL`:

```env
DATABASE_URL=mysql+mysqlconnector://root:mysqlpriya@123@localhost/college_db_orm
```

`models.py` and `migrations/env.py` both load settings from `.env`, so update those values for your local MySQL credentials and database name.

## Running Migrations

1. Create the database in MySQL if it does not exist.
2. Run Alembic migrations:

```bash
alembic upgrade head
```

3. To generate a new migration after model changes:

```bash
alembic revision --autogenerate -m "Your message"
alembic upgrade head
```

## Using the ORM

Run `crud.py` to execute example session operations. It demonstrates:

- inserting departments, students, courses, and enrollments
- querying students by department
- updating a student record
- deleting an enrollment

Example:

```bash
python crud.py
```

## Notes

- `models.py` currently includes an engine with `echo=True`, which logs SQL statements.
- `crud.py` imports `Professor` from `models.py`, but the `Professor` model is not defined in the current `models.py` file; update or remove that import if needed.
- If you change model definitions, regenerate and apply Alembic migrations to keep the schema in sync.

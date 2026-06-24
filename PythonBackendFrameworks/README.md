# Python Backend Frameworks - Training Repository

A comprehensive training repository covering multiple Python backend frameworks and architectural patterns.

## 📁 Project Structure

### 1. **fastAPI_courseAPI**
FastAPI-based REST API for course management with modern async capabilities.

**Features:**
- FastAPI framework with async/await support
- SQLite database integration
- Authentication & security
- Automated API documentation (Swagger/OpenAPI)

**Key Files:**
- `app.py` - Main application entry point
- `database.py` - Database configuration & connection
- `models.py` - SQLAlchemy ORM models
- `schemas.py` - Pydantic validation schemas
- `security.py` - Authentication & JWT handling
- `test.py` - Unit tests

**Setup:**
```bash
cd fastAPI_courseAPI
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
python app.py
```

**API Documentation:** http://localhost:8000/docs

---

### 2. **flask_coursemanager**
Traditional Flask application with SQLAlchemy ORM and database migrations.

**Features:**
- Flask web framework
- Blueprints for modular design
- Alembic database migrations
- SQLite database
- Jinja2 templates

**Project Structure:**
```
flask_coursemanager/
├── app.py              # Main Flask app
├── config.py           # Configuration
├── courses/            # Blueprint for courses routes
│   ├── __init__.py
│   └── routes.py
├── templates/          # HTML templates
├── migrations/         # Alembic migrations
└── hands_on_5/         # Extended version with additional features
```

**Setup:**
```bash
cd flask_coursemanager
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
python app.py
```

**Database Migrations:**
```bash
alembic revision --autogenerate -m "message"
alembic upgrade head
```

---

### 3. **microservices_project**
Microservices architecture with independent services and API gateway.

**Services:**
- **Gateway** - API Gateway for routing requests
- **Student Service** - Student management & enrollment
- **Course Service** - Course management

**Architecture:**
```
Gateway (Port 5000)
├── → Student Service (Port 5001)
├── → Course Service (Port 5002)
└── → Auth Service (conceptual)
```

**Service Responsibilities:**
| Service | Responsibility | Database |
|---------|---|---|
| Student Service | Student management & enrollment | students.db |
| Course Service | Course management | courses.db |
| Gateway | Request routing & load balancing | - |

**Communication Patterns:**
- **Synchronous:** HTTP REST calls (simple, tight coupling)
- **Asynchronous:** RabbitMQ/Kafka (loose coupling, eventual consistency)

**Setup:**
```bash
# Terminal 1 - Gateway
cd microservices_project/gateway
python app.py

# Terminal 2 - Student Service
cd microservices_project/student_service
python app.py

# Terminal 3 - Course Service
cd microservices_project/course_service
python app.py
```

---

### 4. **priya/** - Django Course Manager
Full Django application with REST APIs and database migrations.

**Features:**
- Django ORM
- Django REST Framework
- Serializers for data validation
- User authentication
- Database migrations
- Admin interface

**Project Structure:**
```
priya/coursemanager/
├── manage.py           # Django management script
├── coursemanager/      # Project settings
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
└── courses/            # Django app
    ├── models.py       # Database models
    ├── views.py        # API views
    ├── serializers.py  # DRF serializers
    ├── urls.py         # URL routing
    └── tests.py        # Unit tests
```

**Setup:**
```bash
cd priya/coursemanager
python manage.py migrate
python manage.py runserver
```

**Admin Interface:** http://localhost:8000/admin

---

## 🚀 Quick Start

### Requirements
- Python 3.8+
- pip
- Virtual environment tool (venv)

### General Setup Pattern
```bash
# Clone/navigate to the project
cd <project_directory>

# Create virtual environment
python -m venv venv  # or .venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

---

## 📋 Key Concepts Covered

### Framework Comparisons
| Feature | FastAPI | Flask | Django |
|---------|---------|-------|--------|
| Setup Speed | Very Fast | Fast | Moderate |
| Built-in ORM | No (SQLAlchemy) | No | Yes |
| Built-in Admin | No | No | Yes |
| Async Support | Native | Via Async/Await | Limited |
| REST Framework | Via pydantic | Manual/Flask-RESTful | DRF |
| Learning Curve | Moderate | Easy | Steep |

### Architecture Patterns
- **Monolithic:** FastAPI, Flask (single codebase)
- **Modular:** Flask with Blueprints
- **Microservices:** Gateway + Independent services
- **Full-featured:** Django with batteries included

### Database Integration
- **SQLAlchemy ORM** - FastAPI & Flask
- **Django ORM** - Django
- **Migrations** - Alembic (FastAPI/Flask), Django migrations
- **Relationships** - One-to-Many, Many-to-Many, Foreign Keys

---

## ⚠️ .gitignore Notice

This repository includes a `.gitignore` file that excludes:
- Virtual environments (`venv/`, `.venv/`)
- Python cache (`__pycache__/`, `*.pyc`)
- Database files (`*.db`, `*.sqlite3`)
- Log files (`*.log`)
- Environment files (`.env`)
- Flask instance folders

**Do NOT commit these files** - they contain local configuration and should be regenerated locally.

---

## 🧪 Testing

### FastAPI
```bash
cd fastAPI_courseAPI
pytest test.py -v
```

### Django
```bash
cd priya/coursemanager
python manage.py test
```

---

## 📚 Learning Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Django Documentation](https://docs.djangoproject.com/)
- [SQLAlchemy ORM Tutorial](https://docs.sqlalchemy.org/tutorial/)
- [Microservices Architecture](https://microservices.io/)

---

## 🔧 Troubleshooting

### Database Issues
```bash
# Reset database (WARNING: Deletes data)
rm *.db *.sqlite3
python app.py  # Recreates tables
```

### Virtual Environment Issues
```bash
# Remove and recreate
rm -r venv .venv
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Module Import Errors
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

---

## 📝 Notes

- Each project can run independently
- Use different ports to run multiple services simultaneously
- Check individual project READMEs for specific instructions
- Database migrations should be version controlled (not `.db` files)

---

**Last Updated:** 2026-06-24

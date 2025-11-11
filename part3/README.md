# HBnB Evolution - Part 3: Authentication & Database Integration

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-red.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Database Schema](#database-schema)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Authentication](#authentication)
- [Testing](#testing)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [Authors](#authors)
- [License](#license)

## 🎯 Overview

HBnB Evolution Part 3 is an enhanced backend application that extends the previous parts by introducing:
- **JWT-based authentication** for secure user sessions
- **Role-based access control** (RBAC) with admin privileges
- **Database persistence** using SQLAlchemy ORM
- **SQLite** for development and **MySQL** for production
- **RESTful API** with protected endpoints

This is part of the Holberton School curriculum project [C#27] HBnB v2, focusing on building a scalable, production-ready backend for a rental property management system similar to AirBnB.

## ✨ Features

### Authentication & Authorization
- ✅ JWT token-based authentication using `flask-jwt-extended`
- ✅ Secure password hashing with bcrypt
- ✅ Role-based access control (regular users vs administrators)
- ✅ Protected endpoints requiring authentication
- ✅ Token expiration and refresh mechanisms

### Database Integration
- ✅ SQLAlchemy ORM for database operations
- ✅ SQLite for development environment
- ✅ MySQL support for production environment
- ✅ Automated schema migrations
- ✅ Relationship mapping between entities

### API Capabilities
- ✅ Full CRUD operations for Users, Places, Reviews, and Amenities
- ✅ Ownership validation for user-created content
- ✅ Public endpoints for browsing listings
- ✅ Admin-only endpoints for system management
- ✅ Input validation and error handling

### Data Models
- **User**: Authentication and profile management
- **Place**: Rental property listings with location data
- **Review**: User reviews with ratings (0-5 stars)
- **Amenity**: Available amenities (WiFi, Pool, Parking, etc.)
- **Place-Amenity**: Many-to-many relationship

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│                   API Layer (Flask)                  │
│                  /api/v1/* endpoints                 │
└────────────────────┬────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────┐
│              Business Logic Layer                    │
│         (Facade Pattern + Services)                  │
└────────────────────┬────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────┐
│            Persistence Layer                         │
│   (Repository Pattern + SQLAlchemy ORM)              │
└────────────────────┬────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────┐
│                Database Layer                        │
│          SQLite (dev) / MySQL (prod)                 │
└─────────────────────────────────────────────────────┘
```

### Design Patterns Used
- **Application Factory**: Flask app initialization with configuration
- **Repository Pattern**: Abstract data access layer
- **Facade Pattern**: Simplified interface to complex subsystems
- **Dependency Injection**: Loose coupling between components

## 🗄️ Database Schema

### Entity-Relationship Diagram

```mermaid
erDiagram
    users ||--o{ places : owns
    users ||--o{ reviews : writes
    places ||--o{ reviews : has
    places }o--o{ amenities : contains

    users {
        varchar(60) id PK
        datetime created_at
        datetime updated_at
        varchar(120) email UK
        varchar(128) password
        varchar(50) first_name
        varchar(50) last_name
        boolean is_admin
    }

    places {
        varchar(60) id PK
        datetime created_at
        datetime updated_at
        varchar(100) name
        text description
        float price
        float latitude
        float longitude
        varchar(60) owner_id FK
    }

    reviews {
        varchar(60) id PK
        datetime created_at
        datetime updated_at
        text text
        varchar(60) user_id FK
        varchar(60) place_id FK
        integer rating
    }

    amenities {
        varchar(60) id PK
        datetime created_at
        datetime updated_at
        varchar(50) name
    }
```

For a detailed ER diagram, see [ER_DIAGRAM.md](./ER_DIAGRAM.md).

### Relationships

| Relationship | Type | Description |
|-------------|------|-------------|
| User → Place | One-to-Many | A user can own multiple places |
| User → Review | One-to-Many | A user can write multiple reviews |
| Place → Review | One-to-Many | A place can have multiple reviews |
| Place ↔ Amenity | Many-to-Many | Places can have multiple amenities |

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- MySQL (for production) or SQLite (for development)
- Git

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/holbertonschool-hbnb.git
cd holbertonschool-hbnb/part3
```

### Step 2: Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Set Up Database

#### For Development (SQLite)

```bash
# Run the schema script
python3 -c "from app import create_app, db; app = create_app('development'); app.app_context().push(); db.create_all()"

# Or use SQL scripts
sqlite3 instance/hbnb_dev.db < sql_scripts/schema.sql
sqlite3 instance/hbnb_dev.db < sql_scripts/initial_data.sql
```

#### For Production (MySQL)

```bash
# Create database
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS hbnb_prod;"
mysql -u root -p -e "CREATE USER IF NOT EXISTS 'hbnb_user'@'localhost' IDENTIFIED BY 'hbnb_pwd';"
mysql -u root -p -e "GRANT ALL PRIVILEGES ON hbnb_prod.* TO 'hbnb_user'@'localhost';"
mysql -u root -p -e "FLUSH PRIVILEGES;"

# Run schema
mysql -u hbnb_user -p hbnb_prod < sql_scripts/schema.sql
mysql -u hbnb_user -p hbnb_prod < sql_scripts/initial_data.sql
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
# Flask Configuration
FLASK_APP=run.py
FLASK_ENV=development  # or production

# Secret Keys
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here

# Database Configuration
DATABASE_URL=sqlite:///hbnb_dev.db  # or mysql+pymysql://user:password@localhost/hbnb_prod

# JWT Configuration
JWT_ACCESS_TOKEN_EXPIRES=3600  # 1 hour in seconds
```

### Configuration Classes

The application supports three configuration modes:

- **Development**: SQLite database, debug mode enabled
- **Testing**: In-memory SQLite, for running tests
- **Production**: MySQL database, debug mode disabled

Configure in `config.py`:

```python
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
```

## 🎮 Usage

### Starting the Server

```bash
# Development mode
python run.py

# Or with Flask CLI
flask run

# Production mode with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

The API will be available at `http://localhost:5000/`

### Initial Admin Account

After running `initial_data.sql`, you'll have an admin account:

- **Email**: `admin@hbnb.com`
- **Password**: `admin123`

**⚠️ Change this password in production!**

## 📡 API Endpoints

### Public Endpoints (No Authentication Required)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/places/` | List all places |
| GET | `/api/v1/places/<id>` | Get place details |
| GET | `/api/v1/amenities/` | List all amenities |
| GET | `/api/v1/amenities/<id>` | Get amenity details |

### Authentication Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/register` | Register new user |
| POST | `/api/v1/auth/login` | Login and get JWT token |

### Protected Endpoints (Authentication Required)

#### User Operations

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/api/v1/users/` | List all users | Admin |
| GET | `/api/v1/users/<id>` | Get user details | Owner/Admin |
| PUT | `/api/v1/users/<id>` | Update user | Owner/Admin |
| DELETE | `/api/v1/users/<id>` | Delete user | Admin |

#### Place Operations

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| POST | `/api/v1/places/` | Create place | Authenticated |
| PUT | `/api/v1/places/<id>` | Update place | Owner/Admin |
| DELETE | `/api/v1/places/<id>` | Delete place | Owner/Admin |

#### Review Operations

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| POST | `/api/v1/reviews/` | Create review | Authenticated |
| PUT | `/api/v1/reviews/<id>` | Update review | Owner/Admin |
| DELETE | `/api/v1/reviews/<id>` | Delete review | Owner/Admin |
| GET | `/api/v1/places/<id>/reviews` | Get place reviews | Public |

#### Amenity Operations

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| POST | `/api/v1/amenities/` | Create amenity | Admin |
| PUT | `/api/v1/amenities/<id>` | Update amenity | Admin |
| DELETE | `/api/v1/amenities/<id>` | Delete amenity | Admin |

## 🔐 Authentication

### Login Flow

1. **Register a user**:
```bash
curl -X POST http://localhost:5000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword",
    "first_name": "John",
    "last_name": "Doe"
  }'
```

2. **Login to get token**:
```bash
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword"
  }'
```

Response:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

3. **Use token in requests**:
```bash
curl -X GET http://localhost:5000/api/v1/users/me \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..."
```

### Authorization Rules

#### Regular Users Can:
- ✅ Create places and reviews
- ✅ Update/delete their own places and reviews
- ✅ View all public listings
- ✅ Update their own profile (except email and password)

#### Regular Users Cannot:
- ❌ Review their own places
- ❌ Review the same place twice
- ❌ Modify other users' content
- ❌ Create or modify amenities
- ❌ Change email or password

#### Administrators Can:
- ✅ All regular user actions
- ✅ Create, update, delete any user
- ✅ Modify any place or review
- ✅ Create and modify amenities
- ✅ Change any user's email and password
- ✅ Bypass ownership restrictions

## 🧪 Testing

### Run Unit Tests

```bash
# Run all tests
python -m pytest tests/

# Run with coverage
python -m pytest --cov=app tests/

# Run specific test file
python -m pytest tests/test_users.py
```

### Test API with cURL

```bash
# Run the provided test scripts
./test_api.sh
./test_user_endpoints.sh
./test_place_endpoints.sh
./test_review_endpoints.sh
./test_amenity_endpoints.sh
./test_task3.sh
./test_task4_admin.sh
```

### Test Database with SQL

```bash
# Run CRUD tests
mysql -u hbnb_user -p hbnb_dev < sql_scripts/test_crud.sql

# Or with SQLite
sqlite3 instance/hbnb_dev.db < sql_scripts/test_crud.sql
```

## 📁 Project Structure

```
part3/
├── app.py                      # Application entry point
├── run.py                      # Flask application runner
├── config.py                   # Configuration classes
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── ER_DIAGRAM.md              # Database ER diagram
├── TASKS_8_9_10_SUMMARY.md    # Implementation summary
│
├── hbnb/                       # Main application package
│   ├── __init__.py            # Application factory
│   ├── api/                   # API layer
│   │   └── v1/                # API version 1
│   │       ├── __init__.py
│   │       ├── users.py       # User endpoints
│   │       ├── places.py      # Place endpoints
│   │       ├── reviews.py     # Review endpoints
│   │       └── amenities.py   # Amenity endpoints
│   │
│   ├── bl/                    # Business Logic layer
│   │   ├── __init__.py
│   │   ├── base.py            # Base model with SQLAlchemy
│   │   ├── user.py            # User model
│   │   ├── place.py           # Place model
│   │   ├── review.py          # Review model
│   │   └── amenity.py         # Amenity model
│   │
│   ├── persistence/           # Persistence layer
│   │   ├── __init__.py
│   │   ├── repository.py      # Base repository interface
│   │   ├── sqlalchemy_repo.py # SQLAlchemy repository
│   │   ├── user_repository.py # User-specific repository
│   │   └── memory_repo.py     # In-memory repository (legacy)
│   │
│   ├── facade.py              # Facade pattern implementation
│   ├── errors.py              # Custom error classes
│   └── utils.py               # Utility functions
│
├── sql_scripts/               # SQL database scripts
│   ├── README.md              # SQL scripts documentation
│   ├── schema.sql             # Database schema
│   ├── initial_data.sql       # Initial data population
│   └── test_crud.sql          # CRUD operation tests
│
├── tests/                     # Test suite
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_users.py
│   ├── test_places.py
│   ├── test_reviews.py
│   ├── test_amenities.py
│   └── test_repository.py
│
└── instance/                  # Instance-specific files
    └── hbnb_dev.db           # SQLite database (dev)
```

## 🤝 Contributing

### Development Workflow

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Style

- Follow PEP 8 Python style guide
- Use docstrings for all classes and functions
- Write unit tests for new features
- Keep functions small and focused

### Commit Messages

Follow the conventional commits specification:

```
feat: add user authentication
fix: resolve database connection issue
docs: update API documentation
test: add tests for place endpoints
refactor: simplify facade implementation
```

## 👥 Authors

**Team Members**:
- Student 1 - [GitHub](https://github.com/student1)
- Student 2 - [GitHub](https://github.com/student2)
- Student 3 - [GitHub](https://github.com/student3)

**Project**: Holberton School - [C#27] HBnB v2
**Part**: Part 3 - Authentication & Database Integration

## 📝 License

This project is part of the Holberton School curriculum.
© 2024 Holberton School. All rights reserved.

## 🎓 Learning Objectives

By completing this project, you will have learned to:

- ✅ Implement JWT authentication in Flask applications
- ✅ Secure APIs with role-based access control (RBAC)
- ✅ Use SQLAlchemy ORM for database operations
- ✅ Design and implement relational database schemas
- ✅ Apply the Repository and Facade design patterns
- ✅ Handle user authentication and authorization
- ✅ Secure password storage with bcrypt hashing
- ✅ Configure applications for different environments
- ✅ Write comprehensive API tests
- ✅ Document database schemas with ER diagrams

## 📚 Additional Resources

### Documentation
- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/)
- [Flask-Bcrypt](https://flask-bcrypt.readthedocs.io/)

### Tutorials
- [JWT Authentication Best Practices](https://jwt.io/introduction)
- [SQLAlchemy ORM Tutorial](https://docs.sqlalchemy.org/en/14/orm/tutorial.html)
- [RESTful API Design](https://restfulapi.net/)

### Related Projects
- [Part 1: Modular Architecture](../part1/)
- [Part 2: Business Logic Implementation](../part2/)
- [Part 4: Web Client](../part4/)

## 🐛 Known Issues

- None at this time

## 🔮 Future Enhancements

- [ ] Implement refresh tokens for JWT
- [ ] Add email verification for new users
- [ ] Implement password reset functionality
- [ ] Add rate limiting to prevent abuse
- [ ] Implement file upload for place images
- [ ] Add full-text search for places
- [ ] Implement caching with Redis
- [ ] Add API versioning support
- [ ] Create admin dashboard
- [ ] Add pagination for list endpoints

## 📞 Support

For questions or issues:

1. Check the [FAQ](./FAQ.md)
2. Review existing [Issues](https://github.com/yourusername/holbertonschool-hbnb/issues)
3. Create a new issue with detailed description
4. Contact the teaching staff

## 🙏 Acknowledgments

- Holberton School staff and mentors
- Flask and SQLAlchemy communities
- All contributors and reviewers

---

**Made with ❤️ by Holberton School Students**

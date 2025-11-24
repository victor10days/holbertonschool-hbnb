# HBnB Evolution - Complete Full-Stack Rental Platform

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-red.svg)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-yellow.svg)

A complete, production-ready rental property management platform built progressively through four development phases. This project demonstrates modern software architecture, RESTful API design, database integration, authentication, and full-stack web development.

## Table of Contents

- [Overview](#overview)
- [Project Evolution](#project-evolution)
- [Key Features](#key-features)
- [Tech Stack](#tech-stack)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Architecture](#architecture)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Development Roadmap](#development-roadmap)
- [License](#license)

## Overview

HBnB Evolution is a comprehensive rental property management system similar to AirBnB, built as part of the Holberton School curriculum. The project showcases:

- **Clean Architecture**: Separation of concerns with 3-layer architecture (Presentation, Business Logic, Persistence)
- **Design Patterns**: Facade, Repository, Factory patterns
- **RESTful API**: Complete CRUD operations with proper HTTP semantics
- **Authentication**: JWT-based authentication with role-based access control
- **Database Integration**: SQLAlchemy ORM with SQLite/MySQL support
- **Modern Frontend**: Responsive web interface with vanilla JavaScript
- **Comprehensive Testing**: Unit tests, integration tests, and API tests

## Project Evolution

This project was built in four progressive phases, each adding new capabilities:

### Part 1: Architecture & UML Design
**Focus**: System design and documentation

- Comprehensive UML diagrams (Package, Class, and 7 Sequence diagrams)
- 3-layer architecture design (Presentation, Business Logic, Persistence)
- Entity relationship modeling
- API flow documentation

**[View Part 1 →](part1/)**

### Part 2: Business Logic & API
**Focus**: Core functionality and REST API

- Implemented all business logic models (User, Place, Review, Amenity)
- Flask REST API with Swagger documentation
- In-memory repository for data persistence
- Facade pattern for clean layer communication
- Comprehensive error handling and validation

**[View Part 2 →](part2/)**

### Part 3: Authentication & Database
**Focus**: Security and data persistence

- JWT token-based authentication
- Role-based access control (RBAC)
- SQLAlchemy ORM integration
- Database schema design and implementation
- SQLite (dev) and MySQL (prod) support
- Protected endpoints with ownership validation

**[View Part 3 →](part3/)**

### Part 4: Web Frontend
**Focus**: User interface and client-side functionality

- Responsive HTML/CSS interface
- JavaScript SPA with authentication
- Dynamic place listings with filtering
- Review submission system
- Protected routes and auth state management

**[View Part 4 →](part4/)**

## Key Features

### For Users
- Browse rental properties with price filtering
- View detailed property information with amenities
- Read reviews and ratings from other users
- Create an account and authenticate securely
- Submit reviews for properties (authenticated users only)
- Manage personal listings

### For Administrators
- Full CRUD operations on all entities
- User management and role assignment
- Create and manage amenities
- System-wide content moderation
- Bypass ownership restrictions

### Technical Features
- **RESTful API** with complete CRUD operations
- **JWT Authentication** with token expiration
- **Role-Based Access Control** (regular users vs admins)
- **Data Validation** at multiple layers
- **Error Handling** with proper HTTP status codes
- **Database Relationships** (One-to-Many, Many-to-Many)
- **Repository Pattern** for easy database swapping
- **Facade Pattern** for simplified business logic access
- **Swagger Documentation** for API endpoints

## Tech Stack

### Backend
- **Python 3.8+**
- **Flask 2.0+** - Web framework
- **SQLAlchemy 2.0+** - ORM
- **Flask-JWT-Extended** - JWT authentication
- **Flask-Bcrypt** - Password hashing
- **Flask-RESTX** - API documentation
- **Flask-CORS** - Cross-origin resource sharing

### Frontend
- **HTML5** - Structure
- **CSS3** - Styling with Grid/Flexbox
- **JavaScript ES6+** - Dynamic functionality
- **Fetch API** - HTTP requests

### Database
- **SQLite** - Development
- **MySQL** - Production

### Development Tools
- **pytest** - Testing framework
- **curl** - API testing
- **Git** - Version control

## Quick Start

### Prerequisites
```bash
# Required
Python 3.8+
pip (Python package manager)

# Optional (for production)
MySQL 5.7+
```

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/holbertonschool-hbnb.git
cd holbertonschool-hbnb
```

2. **Choose which part to run** (Part 3 is recommended for full functionality)

#### Running Part 3 (Backend with Auth & Database)
```bash
cd part3

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Initialize database
python3 -c "from app import create_app, db; app = create_app('development'); app.app_context().push(); db.create_all()"

# Run the application
python run.py
```

API will be available at: `http://localhost:5000`
Swagger docs at: `http://localhost:5000/api/v1/docs` (if available)

#### Running Part 4 (Frontend)
```bash
cd part4

# Option 1: Open directly in browser
open index.html

# Option 2: Use a development server
python -m http.server 8000
# Then navigate to http://localhost:8000
```

**Note**: Make sure Part 3 backend is running for the frontend to work properly.

### First Steps

1. **Create an admin account** (via API or use default from initial_data.sql)
```bash
curl -X POST http://localhost:5000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@test.com",
    "password": "admin123",
    "first_name": "Admin",
    "last_name": "User"
  }'
```

2. **Login to get JWT token**
```bash
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@test.com",
    "password": "admin123"
  }'
```

3. **Create a place**
```bash
curl -X POST http://localhost:5000/api/v1/places \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "name": "Cozy Downtown Loft",
    "description": "Beautiful apartment in the heart of the city",
    "price": 120.00,
    "latitude": 40.7128,
    "longitude": -74.0060,
    "owner_id": "YOUR_USER_ID",
    "amenity_ids": []
  }'
```

## Project Structure

```
holbertonschool-hbnb/
├── README.md                    # This file
├── part1/                       # Architecture & UML Design
│   ├── INDEX.md                # Diagram navigation guide
│   ├── UML-DIAGRAMS-README.md  # Detailed UML documentation
│   └── *.mmd                   # Mermaid diagram files
│
├── part2/                       # Business Logic & API
│   ├── README.md               # Part 2 documentation
│   ├── QUICKSTART.md           # Quick setup guide
│   ├── run.py                  # Application entry point
│   ├── config.py               # Configuration classes
│   ├── requirements.txt        # Python dependencies
│   ├── hbnb/                   # Main application package
│   │   ├── api/               # API endpoints
│   │   ├── bl/                # Business logic models
│   │   ├── persistence/       # In-memory repository
│   │   ├── facade.py          # Facade pattern implementation
│   │   ├── errors.py          # Custom exceptions
│   │   └── utils.py           # Utility functions
│   └── tests/                 # Test suite
│
├── part3/                       # Authentication & Database
│   ├── README.md               # Part 3 documentation
│   ├── QUICKSTART.md           # Quick setup guide
│   ├── run.py                  # Application entry point
│   ├── config.py               # Configuration classes
│   ├── requirements.txt        # Python dependencies
│   ├── hbnb/                   # Main application package
│   │   ├── api/               # API endpoints with auth
│   │   ├── bl/                # SQLAlchemy models
│   │   ├── persistence/       # Database repositories
│   │   ├── facade.py          # Facade pattern implementation
│   │   ├── errors.py          # Custom exceptions
│   │   └── utils.py           # Utility functions
│   ├── sql_scripts/           # Database scripts
│   │   ├── schema.sql         # Database schema
│   │   └── initial_data.sql   # Sample data
│   └── tests/                 # Test suite
│
└── part4/                       # Web Frontend
    ├── README.md               # Part 4 documentation
    ├── index.html              # Main page (place listings)
    ├── login.html              # Authentication page
    ├── place.html              # Place details page
    ├── add_review.html         # Review submission page
    ├── scripts.js              # JavaScript functionality
    ├── styles.css              # Application styling
    └── images/                 # Image assets
```

## Architecture

### 3-Layer Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  Presentation Layer                      │
│        (Flask API Routes / HTML Frontend)                │
│              /api/v1/* endpoints                         │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│              Business Logic Layer                        │
│         (Models + Facade + Validation)                   │
│  User | Place | Review | Amenity | HBnBFacade          │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│              Persistence Layer                           │
│         (Repository Pattern + ORM)                       │
│     InMemoryRepository / SQLAlchemyRepository            │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│                  Data Layer                              │
│          SQLite (dev) / MySQL (prod)                     │
└─────────────────────────────────────────────────────────┘
```

### Design Patterns

- **Application Factory**: Flask app initialization with different configurations
- **Repository Pattern**: Abstract data access layer for easy database swapping
- **Facade Pattern**: Simplified interface to complex business logic
- **Dependency Injection**: Loose coupling between layers

### Data Model

```
User
├── id (PK)
├── email (unique)
├── password (hashed)
├── first_name
├── last_name
├── is_admin
└── relationships
    ├── places (1:N)
    └── reviews (1:N)

Place
├── id (PK)
├── name
├── description
├── price
├── latitude
├── longitude
├── owner_id (FK → User)
└── relationships
    ├── owner (N:1 → User)
    ├── reviews (1:N)
    └── amenities (N:M)

Review
├── id (PK)
├── text
├── rating (1-5)
├── user_id (FK → User)
├── place_id (FK → Place)
└── relationships
    ├── user (N:1 → User)
    └── place (N:1 → Place)

Amenity
├── id (PK)
├── name
└── relationships
    └── places (N:M)
```

## API Documentation

### Base URL
```
http://localhost:5000/api/v1
```

### Authentication Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/auth/register` | Register new user | No |
| POST | `/auth/login` | Login and get JWT token | No |

### User Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/users` | List all users | Admin |
| GET | `/users/<id>` | Get user details | Owner/Admin |
| PUT | `/users/<id>` | Update user | Owner/Admin |
| DELETE | `/users/<id>` | Delete user | Admin |

### Place Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/places` | List all places | No |
| GET | `/places/<id>` | Get place details | No |
| POST | `/places` | Create place | Yes |
| PUT | `/places/<id>` | Update place | Owner/Admin |
| DELETE | `/places/<id>` | Delete place | Owner/Admin |

### Review Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/reviews` | List all reviews | No |
| GET | `/reviews/<id>` | Get review details | No |
| POST | `/reviews` | Create review | Yes |
| PUT | `/reviews/<id>` | Update review | Owner/Admin |
| DELETE | `/reviews/<id>` | Delete review | Owner/Admin |
| GET | `/places/<id>/reviews` | Get place reviews | No |

### Amenity Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/amenities` | List all amenities | No |
| GET | `/amenities/<id>` | Get amenity details | No |
| POST | `/amenities` | Create amenity | Admin |
| PUT | `/amenities/<id>` | Update amenity | Admin |
| DELETE | `/amenities/<id>` | Delete amenity | Admin |

### Example API Calls

**Register User**
```bash
curl -X POST http://localhost:5000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepass",
    "first_name": "John",
    "last_name": "Doe"
  }'
```

**Create Place (requires auth)**
```bash
curl -X POST http://localhost:5000/api/v1/places \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "name": "Beach House",
    "description": "Beautiful oceanfront property",
    "price": 250.00,
    "latitude": 34.0522,
    "longitude": -118.2437,
    "owner_id": "user-id-here",
    "amenity_ids": []
  }'
```

## Testing

### Backend Tests

```bash
# Part 2 - Business Logic Tests
cd part2
python -m unittest discover -s tests -v

# Part 3 - Database & Auth Tests
cd part3
python -m pytest tests/ -v
python -m pytest --cov=app tests/  # With coverage
```

### API Testing with cURL

```bash
# Part 3 includes test scripts
cd part3
./test_api.sh
./test_user_endpoints.sh
./test_place_endpoints.sh
./test_review_endpoints.sh
```

### Frontend Testing

1. Open the browser console
2. Check for JavaScript errors
3. Test authentication flow
4. Test CRUD operations via UI
5. Verify responsive design on different screen sizes

## Development Roadmap

### Completed
- [x] UML architecture design
- [x] Business logic implementation
- [x] REST API with Swagger docs
- [x] In-memory data persistence
- [x] JWT authentication
- [x] Role-based access control
- [x] SQLAlchemy database integration
- [x] MySQL production support
- [x] Web frontend with authentication
- [x] Review system
- [x] Price filtering

### Future Enhancements
- [ ] Email verification for new users
- [ ] Password reset functionality
- [ ] File upload for place images
- [ ] Advanced search and filtering
- [ ] Booking system
- [ ] Payment integration
- [ ] Real-time notifications
- [ ] Admin dashboard
- [ ] API rate limiting
- [ ] Caching with Redis
- [ ] Pagination for list endpoints
- [ ] Docker containerization
- [ ] CI/CD pipeline

## License

This project is part of the Holberton School curriculum.
© 2024 Holberton School. All rights reserved.

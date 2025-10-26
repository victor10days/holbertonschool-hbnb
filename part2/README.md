# HBnB v2 — Part 2 Implementation Pack

Complete implementation of Business Logic + API for HBnB project Part 2.

## Features

- ✅ Clean 3-layer architecture (Presentation, Business Logic, Persistence)
- ✅ In-memory repository (swap-ready for SQLAlchemy in Part 3)
- ✅ Facade pattern for BL ↔ API communication
- ✅ Dataclass-based models with validation
- ✅ Flask + flask-restx with Swagger documentation
- ✅ Extended attributes in responses (owner details, amenities)
- ✅ Comprehensive error handling
- ✅ Full test suite

## Project Structure

```
part2/
├── app.py                      # Flask app factory + API root
├── requirements.txt            # Dependencies
├── hbnb/
│   ├── __init__.py
│   ├── facade.py              # Facade for BL <-> API
│   ├── errors.py              # Error types + handlers
│   ├── utils.py               # Helpers (UUID, timestamps, pagination)
│   ├── persistence/
│   │   ├── __init__.py
│   │   └── memory_repo.py     # In-memory repository
│   ├── bl/                    # Business Logic models
│   │   ├── __init__.py
│   │   ├── base.py           # BaseModel (id, created_at, updated_at)
│   │   ├── user.py           # User model
│   │   ├── amenity.py        # Amenity model
│   │   ├── place.py          # Place model
│   │   └── review.py         # Review model
│   └── api/                   # API endpoints
│       ├── __init__.py
│       └── v1/
│           ├── __init__.py
│           ├── users.py      # /api/v1/users
│           ├── amenities.py  # /api/v1/amenities
│           ├── places.py     # /api/v1/places
│           └── reviews.py    # /api/v1/reviews
└── tests/
    ├── __init__.py
    ├── test_users.py
    ├── test_amenities.py
    ├── test_places.py
    └── test_reviews.py
```

## Setup & Run

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

The API will be available at: **http://localhost:5000**

Swagger UI documentation: **http://localhost:5000/**

## API Endpoints

### Users
- `POST /api/v1/users` - Create user
- `GET /api/v1/users` - List all users
- `GET /api/v1/users/<id>` - Get user by ID
- `PUT /api/v1/users/<id>` - Update user

### Amenities
- `POST /api/v1/amenities` - Create amenity
- `GET /api/v1/amenities` - List all amenities
- `GET /api/v1/amenities/<id>` - Get amenity by ID
- `PUT /api/v1/amenities/<id>` - Update amenity

### Places
- `POST /api/v1/places` - Create place (with owner and amenities validation)
- `GET /api/v1/places` - List all places (with expanded owner & amenities)
- `GET /api/v1/places/<id>` - Get place by ID (with expanded data)
- `PUT /api/v1/places/<id>` - Update place

### Reviews
- `POST /api/v1/reviews` - Create review
- `GET /api/v1/reviews` - List all reviews
- `GET /api/v1/reviews/<id>` - Get review by ID
- `PUT /api/v1/reviews/<id>` - Update review
- `DELETE /api/v1/reviews/<id>` - Delete review
- `GET /api/v1/reviews/place/<place_id>` - Get all reviews for a place

## Testing

Run all tests:
```bash
python -m unittest discover -s tests -v
```

Run specific test:
```bash
python -m unittest tests.test_users
```

## cURL Examples

### Create User
```bash
curl -X POST http://localhost:5000/api/v1/users \
  -H 'Content-Type: application/json' \
  -d '{
    "email": "test@example.com",
    "password": "secret123",
    "first_name": "John",
    "last_name": "Doe"
  }'
```

### Create Amenity
```bash
curl -X POST http://localhost:5000/api/v1/amenities \
  -H 'Content-Type: application/json' \
  -d '{"name": "WiFi"}'
```

### Create Place
```bash
curl -X POST http://localhost:5000/api/v1/places \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "Cozy Loft",
    "description": "Beautiful downtown apartment",
    "price": 100.0,
    "latitude": 40.7128,
    "longitude": -74.0060,
    "owner_id": "<USER_ID>",
    "amenity_ids": ["<AMENITY_ID>"]
  }'
```

### Create Review
```bash
curl -X POST http://localhost:5000/api/v1/reviews \
  -H 'Content-Type: application/json' \
  -d '{
    "text": "Great place!",
    "rating": 5,
    "user_id": "<USER_ID>",
    "place_id": "<PLACE_ID>"
  }'
```

### Delete Review
```bash
curl -X DELETE http://localhost:5000/api/v1/reviews/<REVIEW_ID>
```

## Key Features

### 1. Dataclass Models
All models use Python dataclasses for clean, concise code:
```python
@dataclass
class User(BaseModel):
    email: str = ""
    password: str = ""
    first_name: str = ""
    last_name: str = ""
```

### 2. Validation
Each model has a `validate()` method:
- Email format validation
- Required fields checking
- Range validation (price, coordinates, rating)
- Foreign key validation (owner_id, amenity_ids)

### 3. Extended Attributes
Places include full owner and amenities data in responses:
```json
{
  "id": "...",
  "name": "Cozy Loft",
  "owner": {
    "id": "...",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com"
  },
  "amenities": [
    {"id": "...", "name": "WiFi"},
    {"id": "...", "name": "Pool"}
  ]
}
```

### 4. Error Handling
Custom HTTP exceptions with proper status codes:
- `404 NotFound` - Resource doesn't exist
- `400 BadRequest` - Invalid data or validation error
- `409 Conflict` - Duplicate email (future feature)

### 5. Repository Pattern
Abstract data access for easy database swap in Part 3:
```python
repo.add(obj)
repo.get(Class, id)
repo.list(Class, predicate=None)
repo.update(obj)
repo.delete(Class, id)
```

## Notes for Part 3

The architecture is designed for easy migration to SQLAlchemy:

1. **Replace `MemoryRepository`** with SQLAlchemy session-backed repository
2. **Keep `HbnbFacade` API stable** - only swap repository internals
3. **Add JWT/RBAC** in Presentation layer decorators
4. **Models remain mostly unchanged** - just add SQLAlchemy mappings

## Requirements

- Python 3.10+
- Flask 3.0+
- flask-restx 1.3+

## License

Educational project for Holberton School.

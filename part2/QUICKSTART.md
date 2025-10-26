# HBnB Part 2 - Quick Start Guide

## Installation

```bash
# Navigate to the project directory
cd /Users/Victor/Documents/Holberton/holbertonschool-hbnb/part2

# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # On Mac/Linux
# OR
.venv\Scripts\activate  # On Windows

# Install dependencies
pip install -r requirements.txt
```

## Running the Application

```bash
# Make sure virtual environment is activated
python app.py
```

The server will start at: **http://localhost:5000**

Swagger documentation: **http://localhost:5000/**

## Quick Test

In a new terminal (while the server is running):

```bash
./test_api.sh
```

This will create a user, amenity, place, and show the results.

## Manual Testing with cURL

### 1. Create a User
```bash
curl -X POST http://localhost:5000/api/v1/users \
  -H 'Content-Type: application/json' \
  -d '{
    "email": "john@example.com",
    "password": "secret123",
    "first_name": "John",
    "last_name": "Doe"
  }' | python3 -m json.tool
```

Save the returned `id` for the next steps!

### 2. Create an Amenity
```bash
curl -X POST http://localhost:5000/api/v1/amenities \
  -H 'Content-Type: application/json' \
  -d '{"name": "WiFi"}' | python3 -m json.tool
```

Save the `id`!

### 3. Create a Place
```bash
curl -X POST http://localhost:5000/api/v1/places \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "Cozy Downtown Loft",
    "description": "Beautiful apartment in the city",
    "price": 150.00,
    "latitude": 40.7128,
    "longitude": -74.0060,
    "owner_id": "PUT_USER_ID_HERE",
    "amenity_ids": ["PUT_AMENITY_ID_HERE"]
  }' | python3 -m json.tool
```

### 4. Get Place with Extended Details
```bash
curl http://localhost:5000/api/v1/places/PUT_PLACE_ID_HERE | python3 -m json.tool
```

Notice how the response includes:
- Full owner details (first_name, last_name, email)
- Complete amenity objects (not just IDs)

### 5. Create a Review
```bash
curl -X POST http://localhost:5000/api/v1/reviews \
  -H 'Content-Type: application/json' \
  -d '{
    "text": "Amazing place! Very comfortable and clean.",
    "rating": 5,
    "user_id": "PUT_USER_ID_HERE",
    "place_id": "PUT_PLACE_ID_HERE"
  }' | python3 -m json.tool
```

### 6. Get All Reviews for a Place
```bash
curl http://localhost:5000/api/v1/reviews/place/PUT_PLACE_ID_HERE | python3 -m json.tool
```

### 7. Delete a Review
```bash
curl -X DELETE http://localhost:5000/api/v1/reviews/PUT_REVIEW_ID_HERE
```

Should return status 204 (No Content).

## Running Tests

```bash
# Run all tests
python -m unittest discover -s tests -v

# Run specific test file
python -m unittest tests.test_users -v
python -m unittest tests.test_places -v
python -m unittest tests.test_reviews -v
```

## Key Features to Test

### 1. Data Validation
Try creating invalid data to see validation errors:

```bash
# Invalid email
curl -X POST http://localhost:5000/api/v1/users \
  -H 'Content-Type: application/json' \
  -d '{"email":"notanemail","password":"secret","first_name":"John","last_name":"Doe"}'
# Should return 400 Bad Request

# Negative price
curl -X POST http://localhost:5000/api/v1/places \
  -H 'Content-Type: application/json' \
  -d '{"name":"Test","price":-50,"latitude":0,"longitude":0,"owner_id":"valid-id"}'
# Should return 400 Bad Request

# Invalid rating
curl -X POST http://localhost:5000/api/v1/reviews \
  -H 'Content-Type: application/json' \
  -d '{"text":"Test","rating":10,"user_id":"id","place_id":"id"}'
# Should return 400 Bad Request
```

### 2. Foreign Key Validation
Try creating a place with invalid owner_id:

```bash
curl -X POST http://localhost:5000/api/v1/places \
  -H 'Content-Type: application/json' \
  -d '{
    "name":"Test",
    "price":100,
    "latitude":0,
    "longitude":0,
    "owner_id":"non-existent-id"
  }'
# Should return 400 Bad Request: "owner_id must reference an existing User"
```

### 3. Extended Attributes
Notice how GET /places returns nested owner and amenities:

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

### 4. Password Security
Create a user and notice the password is NOT returned:

```bash
curl -X POST http://localhost:5000/api/v1/users \
  -H 'Content-Type: application/json' \
  -d '{"email":"test@test.com","password":"secret","first_name":"A","last_name":"B"}'
# Response should NOT contain "password" field
```

## Swagger Documentation

Visit **http://localhost:5000/** in your browser to:
- See all available endpoints
- Test endpoints interactively
- View request/response schemas
- Try out the API without cURL

## Troubleshooting

### Port Already in Use
If port 5000 is busy:

```bash
# Find and kill process on port 5000 (Mac/Linux)
lsof -ti:5000 | xargs kill -9

# Or change port in app.py (line 28):
app.run(host="0.0.0.0", port=5001, debug=True)
```

### Import Errors
Make sure you're in the correct directory and virtual environment is activated:

```bash
pwd  # Should show .../holbertonschool-hbnb/part2
which python  # Should show .../part2/.venv/bin/python
```

### Module Not Found
Reinstall dependencies:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## Project Structure Summary

```
part2/
├── app.py                      ← Start here (Flask app)
├── hbnb/
│   ├── facade.py              ← Business logic orchestrator
│   ├── errors.py              ← Custom exceptions
│   ├── bl/                    ← Business Logic (models)
│   │   ├── user.py
│   │   ├── place.py
│   │   ├── review.py
│   │   └── amenity.py
│   ├── api/v1/                ← API endpoints
│   │   ├── users.py
│   │   ├── places.py
│   │   ├── reviews.py
│   │   └── amenities.py
│   └── persistence/
│       └── memory_repo.py     ← In-memory storage
└── tests/                     ← Unit tests
```

## Next Steps

1. **Explore Swagger UI**: Visit http://localhost:5000/
2. **Run Tests**: `python -m unittest discover -s tests -v`
3. **Read the Code**: Start with `app.py`, then `facade.py`, then models in `bl/`
4. **Experiment**: Try creating complex data relationships
5. **Prepare for Part 3**: Think about how to replace `memory_repo.py` with SQLAlchemy

## Common Workflows

### Complete User Journey
```bash
# 1. Register user
USER=$(curl -s -X POST http://localhost:5000/api/v1/users -H 'Content-Type: application/json' -d '{"email":"user@test.com","password":"pw","first_name":"Test","last_name":"User"}')
USER_ID=$(echo $USER | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")

# 2. Create amenities
WIFI=$(curl -s -X POST http://localhost:5000/api/v1/amenities -H 'Content-Type: application/json' -d '{"name":"WiFi"}')
WIFI_ID=$(echo $WIFI | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")

# 3. Create place
PLACE=$(curl -s -X POST http://localhost:5000/api/v1/places -H 'Content-Type: application/json' -d "{\"name\":\"My Place\",\"description\":\"Nice\",\"price\":100,\"latitude\":0,\"longitude\":0,\"owner_id\":\"$USER_ID\",\"amenity_ids\":[\"$WIFI_ID\"]}")
PLACE_ID=$(echo $PLACE | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")

# 4. View place with all details
curl -s http://localhost:5000/api/v1/places/$PLACE_ID | python3 -m json.tool
```

Happy coding! 🚀

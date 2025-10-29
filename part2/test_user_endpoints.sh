#!/bin/bash

echo "=== Testing User API Endpoints ==="
echo

echo "1. Create a user (POST /api/v1/users/) - Should return 201"
USER1=$(curl -s -w "\nHTTP_CODE:%{http_code}" -X POST http://127.0.0.1:5000/api/v1/users/ \
  -H 'Content-Type: application/json' \
  -d '{"email": "user1@example.com", "first_name": "User", "last_name": "One"}')
echo "$USER1"
USER1_ID=$(echo "$USER1" | grep -v "HTTP_CODE" | python3 -c "import sys, json; print(json.load(sys.stdin)['id'])" 2>/dev/null)
echo

echo "2. Try to create user with same email - Should return 400"
curl -s -w "\nHTTP_CODE:%{http_code}\n" -X POST http://127.0.0.1:5000/api/v1/users/ \
  -H 'Content-Type: application/json' \
  -d '{"email": "user1@example.com", "first_name": "Another", "last_name": "User"}'
echo

echo "3. Create user with invalid email - Should return 400"
curl -s -w "\nHTTP_CODE:%{http_code}\n" -X POST http://127.0.0.1:5000/api/v1/users/ \
  -H 'Content-Type: application/json' \
  -d '{"email": "invalid-email", "first_name": "Bad", "last_name": "Email"}'
echo

echo "4. Create user with missing fields - Should return 400"
curl -s -w "\nHTTP_CODE:%{http_code}\n" -X POST http://127.0.0.1:5000/api/v1/users/ \
  -H 'Content-Type: application/json' \
  -d '{"email": "missing@example.com", "first_name": ""}'
echo

echo "5. Get user by ID (GET /api/v1/users/<id>) - Should return 200"
curl -s -w "\nHTTP_CODE:%{http_code}\n" http://127.0.0.1:5000/api/v1/users/$USER1_ID | python3 -m json.tool
echo

echo "6. Get user with invalid ID - Should return 404"
curl -s -w "\nHTTP_CODE:%{http_code}\n" http://127.0.0.1:5000/api/v1/users/invalid-id-123
echo

echo "7. Get list of all users (GET /api/v1/users/) - Should return 200"
curl -s -w "\nHTTP_CODE:%{http_code}\n" http://127.0.0.1:5000/api/v1/users/ | python3 -m json.tool
echo

echo "8. Update user (PUT /api/v1/users/<id>) - Should return 200"
curl -s -w "\nHTTP_CODE:%{http_code}\n" -X PUT http://127.0.0.1:5000/api/v1/users/$USER1_ID \
  -H 'Content-Type: application/json' \
  -d '{"first_name": "Updated", "last_name": "Name"}' | python3 -m json.tool
echo

echo "9. Update user with invalid email - Should return 400"
curl -s -w "\nHTTP_CODE:%{http_code}\n" -X PUT http://127.0.0.1:5000/api/v1/users/$USER1_ID \
  -H 'Content-Type: application/json' \
  -d '{"email": "bad-email"}'
echo

echo "10. Update user with invalid ID - Should return 404"
curl -s -w "\nHTTP_CODE:%{http_code}\n" -X PUT http://127.0.0.1:5000/api/v1/users/nonexistent-id \
  -H 'Content-Type: application/json' \
  -d '{"first_name": "Test"}'
echo

echo "=== All tests completed ==="

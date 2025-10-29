#!/bin/bash

echo "=== Testing Review API Endpoints ==="
echo

# Setup: Create user, place
echo "Setup: Creating user and place..."
USER=$(curl -s -X POST http://127.0.0.1:5000/api/v1/users/ \
  -H 'Content-Type: application/json' \
  -d '{"email": "reviewer@example.com", "first_name": "Reviewer", "last_name": "User"}')
USER_ID=$(echo "$USER" | python3 -c "import sys, json; print(json.load(sys.stdin)['id'])" 2>/dev/null)

OWNER=$(curl -s -X POST http://127.0.0.1:5000/api/v1/users/ \
  -H 'Content-Type: application/json' \
  -d '{"email": "owner@example.com", "first_name": "Owner", "last_name": "User"}')
OWNER_ID=$(echo "$OWNER" | python3 -c "import sys, json; print(json.load(sys.stdin)['id'])" 2>/dev/null)

PLACE=$(curl -s -X POST http://127.0.0.1:5000/api/v1/places/ \
  -H 'Content-Type: application/json' \
  -d "{\"title\": \"Test Place\", \"price\": 100.0, \"latitude\": 40.0, \"longitude\": -70.0, \"owner_id\": \"$OWNER_ID\", \"amenities\": []}")
PLACE_ID=$(echo "$PLACE" | python3 -c "import sys, json; print(json.load(sys.stdin)['id'])" 2>/dev/null)

echo "User ID: $USER_ID"
echo "Place ID: $PLACE_ID"
echo

echo "1. Create review with valid data - Should return 201"
REVIEW1=$(curl -s -w "\nHTTP_CODE:%{http_code}" -X POST http://127.0.0.1:5000/api/v1/reviews/ \
  -H 'Content-Type: application/json' \
  -d "{\"text\": \"Great place!\", \"rating\": 5, \"user_id\": \"$USER_ID\", \"place_id\": \"$PLACE_ID\"}")
echo "$REVIEW1" | python3 -m json.tool 2>/dev/null || echo "$REVIEW1"
REVIEW1_ID=$(echo "$REVIEW1" | grep -v "HTTP_CODE" | python3 -c "import sys, json; print(json.load(sys.stdin)['id'])" 2>/dev/null)
echo

echo "2. Create review with rating 0 (invalid) - Should return 400"
curl -s -w "\nHTTP_CODE:%{http_code}\n" -X POST http://127.0.0.1:5000/api/v1/reviews/ \
  -H 'Content-Type: application/json' \
  -d "{\"text\": \"Bad\", \"rating\": 0, \"user_id\": \"$USER_ID\", \"place_id\": \"$PLACE_ID\"}"
echo

echo "3. Create review with rating 6 (invalid) - Should return 400"
curl -s -w "\nHTTP_CODE:%{http_code}\n" -X POST http://127.0.0.1:5000/api/v1/reviews/ \
  -H 'Content-Type: application/json' \
  -d "{\"text\": \"Too high\", \"rating\": 6, \"user_id\": \"$USER_ID\", \"place_id\": \"$PLACE_ID\"}"
echo

echo "4. Create review with empty text - Should return 400"
curl -s -w "\nHTTP_CODE:%{http_code}\n" -X POST http://127.0.0.1:5000/api/v1/reviews/ \
  -H 'Content-Type: application/json' \
  -d "{\"text\": \"\", \"rating\": 5, \"user_id\": \"$USER_ID\", \"place_id\": \"$PLACE_ID\"}"
echo

echo "5. Create review with non-existent user - Should return 400"
curl -s -w "\nHTTP_CODE:%{http_code}\n" -X POST http://127.0.0.1:5000/api/v1/reviews/ \
  -H 'Content-Type: application/json' \
  -d "{\"text\": \"Test\", \"rating\": 5, \"user_id\": \"invalid-user-id\", \"place_id\": \"$PLACE_ID\"}"
echo

echo "6. Create review with non-existent place - Should return 400"
curl -s -w "\nHTTP_CODE:%{http_code}\n" -X POST http://127.0.0.1:5000/api/v1/reviews/ \
  -H 'Content-Type: application/json' \
  -d "{\"text\": \"Test\", \"rating\": 5, \"user_id\": \"$USER_ID\", \"place_id\": \"invalid-place-id\"}"
echo

echo "7. Get review by ID - Should return 200"
curl -s http://127.0.0.1:5000/api/v1/reviews/$REVIEW1_ID | python3 -m json.tool
echo "HTTP_CODE:200"
echo

echo "8. Get review with invalid ID - Should return 404"
curl -s -w "\nHTTP_CODE:%{http_code}\n" http://127.0.0.1:5000/api/v1/reviews/invalid-id
echo

echo "9. Get reviews by place - Should return 200"
curl -s http://127.0.0.1:5000/api/v1/places/$PLACE_ID/reviews | python3 -m json.tool
echo "HTTP_CODE:200"
echo

echo "10. Update review with valid data - Should return 200"
curl -s -w "\nHTTP_CODE:%{http_code}\n" -X PUT http://127.0.0.1:5000/api/v1/reviews/$REVIEW1_ID \
  -H 'Content-Type: application/json' \
  -d '{"text": "Updated review", "rating": 4}' | python3 -m json.tool
echo

echo "11. Update review with invalid rating - Should return 400"
curl -s -w "\nHTTP_CODE:%{http_code}\n" -X PUT http://127.0.0.1:5000/api/v1/reviews/$REVIEW1_ID \
  -H 'Content-Type: application/json' \
  -d '{"rating": 0}'
echo

echo "12. Update review with empty text - Should return 400"
curl -s -w "\nHTTP_CODE:%{http_code}\n" -X PUT http://127.0.0.1:5000/api/v1/reviews/$REVIEW1_ID \
  -H 'Content-Type: application/json' \
  -d '{"text": ""}'
echo

echo "13. Delete review - Should return 200"
curl -s -w "\nHTTP_CODE:%{http_code}\n" -X DELETE http://127.0.0.1:5000/api/v1/reviews/$REVIEW1_ID
echo

echo "14. Try to get deleted review - Should return 404"
curl -s -w "\nHTTP_CODE:%{http_code}\n" http://127.0.0.1:5000/api/v1/reviews/$REVIEW1_ID
echo

echo "=== All Review tests completed ==="

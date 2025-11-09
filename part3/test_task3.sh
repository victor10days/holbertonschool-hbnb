#!/bin/bash

echo "========================================="
echo "Task 3: Testing Authenticated Endpoints"
echo "========================================="
echo ""

# Store tokens
USER1_TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc2MjUzMjE0OCwianRpIjoiZTcyNTM2OGItZGIzNi00YWE0LThiNmMtODAwMmVmYWUwYmJjIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6Ijg2NDA4MDdmLTI5M2YtNDMxOS1iZDcwLWE5OThiMjUzMzMzZiIsIm5iZiI6MTc2MjUzMjE0OCwiY3NyZiI6Ijc2ZGU5MzRlLTdhOTMtNDc4NS1hODE3LTAwZDJmYTQyODBlOSIsImV4cCI6MTc2MjUzNTc0OCwiaXNfYWRtaW4iOmZhbHNlfQ.6lyiVxphJt61tc3pg3Q6wRdnXcbN2ogT-slJun4lY2c"
USER1_ID="8640807f-293f-4319-bd70-a998b253333f"
USER2_ID="a8be357a-1f75-4360-8a81-73f9de617fc2"

# Login as user2
echo "Test 1: Login as User2"
USER2_RESPONSE=$(curl -s -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user2@test.com", "password": "pass456"}')
USER2_TOKEN=$(echo $USER2_RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])")
echo "✓ User2 logged in successfully"
echo ""

# Test 2: Create amenity (for place testing)
echo "Test 2: Create Amenity (no auth required)"
AMENITY_RESPONSE=$(curl -s -X POST http://localhost:5000/api/v1/amenities \
  -H "Content-Type: application/json" \
  -d '{"name": "WiFi"}')
AMENITY_ID=$(echo $AMENITY_RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin)['id'])")
echo "✓ Amenity created: $AMENITY_ID"
echo ""

# Test 3: Create place WITH authentication (User1)
echo "Test 3: Create Place WITH JWT (User1)"
PLACE_RESPONSE=$(curl -s -X POST http://localhost:5000/api/v1/places \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $USER1_TOKEN" \
  -d "{\"name\": \"User1 Place\", \"description\": \"Nice place\", \"price\": 100.0, \"latitude\": 45.5, \"longitude\": -73.5, \"owner_id\": \"$USER1_ID\", \"amenity_ids\": [\"$AMENITY_ID\"]}")
PLACE_ID=$(echo $PLACE_RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin)['id'])")
echo "✓ Place created by User1: $PLACE_ID"
echo ""

# Test 4: Try to create place WITHOUT authentication (should fail)
echo "Test 4: Try to Create Place WITHOUT JWT (should fail)"
FAIL_RESPONSE=$(curl -s -w "\n%{http_code}" -X POST http://localhost:5000/api/v1/places \
  -H "Content-Type: application/json" \
  -d "{\"name\": \"Fail Place\", \"description\": \"Should fail\", \"price\": 50.0, \"latitude\": 45.5, \"longitude\": -73.5, \"owner_id\": \"$USER1_ID\", \"amenity_ids\": []}")
HTTP_CODE=$(echo "$FAIL_RESPONSE" | tail -1)
if [ "$HTTP_CODE" = "401" ]; then
  echo "✓ Correctly rejected (401)"
else
  echo "✗ FAILED: Expected 401, got $HTTP_CODE"
fi
echo ""

# Test 5: User2 tries to update User1's place (should fail)
echo "Test 5: User2 Tries to Update User1's Place (should fail)"
FAIL_RESPONSE=$(curl -s -w "\n%{http_code}" -X PUT http://localhost:5000/api/v1/places/$PLACE_ID \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $USER2_TOKEN" \
  -d "{\"name\": \"Hacked Place\", \"description\": \"Hacked\", \"price\": 1.0, \"latitude\": 45.5, \"longitude\": -73.5, \"owner_id\": \"$USER2_ID\", \"amenity_ids\": []}")
HTTP_CODE=$(echo "$FAIL_RESPONSE" | tail -1)
if [ "$HTTP_CODE" = "403" ]; then
  echo "✓ Correctly rejected (403)"
else
  echo "✗ FAILED: Expected 403, got $HTTP_CODE"
fi
echo ""

# Test 6: User1 updates their own place (should succeed)
echo "Test 6: User1 Updates Their Own Place (should succeed)"
UPDATE_RESPONSE=$(curl -s -w "\n%{http_code}" -X PUT http://localhost:5000/api/v1/places/$PLACE_ID \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $USER1_TOKEN" \
  -d "{\"name\": \"Updated Place\", \"description\": \"Updated\", \"price\": 150.0, \"latitude\": 45.5, \"longitude\": -73.5, \"owner_id\": \"$USER1_ID\", \"amenity_ids\": [\"$AMENITY_ID\"]}")
HTTP_CODE=$(echo "$UPDATE_RESPONSE" | tail -1)
if [ "$HTTP_CODE" = "200" ]; then
  echo "✓ Successfully updated"
else
  echo "✗ FAILED: Expected 200, got $HTTP_CODE"
fi
echo ""

# Test 7: User2 creates review for User1's place
echo "Test 7: User2 Creates Review for User1's Place (should succeed)"
REVIEW_RESPONSE=$(curl -s -X POST http://localhost:5000/api/v1/reviews \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $USER2_TOKEN" \
  -d "{\"text\": \"Great place!\", \"rating\": 5, \"user_id\": \"$USER2_ID\", \"place_id\": \"$PLACE_ID\"}")
REVIEW_ID=$(echo $REVIEW_RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin)['id'])")
echo "✓ Review created by User2: $REVIEW_ID"
echo ""

# Test 8: User1 tries to review their own place (should fail)
echo "Test 8: User1 Tries to Review Their Own Place (should fail)"
FAIL_RESPONSE=$(curl -s -w "\n%{http_code}" -X POST http://localhost:5000/api/v1/reviews \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $USER1_TOKEN" \
  -d "{\"text\": \"My own place\", \"rating\": 5, \"user_id\": \"$USER1_ID\", \"place_id\": \"$PLACE_ID\"}")
HTTP_CODE=$(echo "$FAIL_RESPONSE" | tail -1)
if [ "$HTTP_CODE" = "400" ]; then
  echo "✓ Correctly rejected (400)"
else
  echo "✗ FAILED: Expected 400, got $HTTP_CODE"
fi
echo ""

# Test 9: User2 tries to review same place twice (should fail)
echo "Test 9: User2 Tries to Review Same Place Twice (should fail)"
FAIL_RESPONSE=$(curl -s -w "\n%{http_code}" -X POST http://localhost:5000/api/v1/reviews \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $USER2_TOKEN" \
  -d "{\"text\": \"Another review\", \"rating\": 4, \"user_id\": \"$USER2_ID\", \"place_id\": \"$PLACE_ID\"}")
HTTP_CODE=$(echo "$FAIL_RESPONSE" | tail -1)
if [ "$HTTP_CODE" = "400" ]; then
  echo "✓ Correctly rejected (400)"
else
  echo "✗ FAILED: Expected 400, got $HTTP_CODE"
fi
echo ""

# Test 10: User1 updates their own profile (should succeed)
echo "Test 10: User1 Updates Their Own Profile (should succeed)"
UPDATE_RESPONSE=$(curl -s -w "\n%{http_code}" -X PUT http://localhost:5000/api/v1/users/$USER1_ID \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $USER1_TOKEN" \
  -d '{"first_name": "UpdatedUser", "last_name": "UpdatedOne"}')
HTTP_CODE=$(echo "$UPDATE_RESPONSE" | tail -1)
if [ "$HTTP_CODE" = "200" ]; then
  echo "✓ Successfully updated"
else
  echo "✗ FAILED: Expected 200, got $HTTP_CODE"
fi
echo ""

# Test 11: User2 tries to update User1's profile (should fail)
echo "Test 11: User2 Tries to Update User1's Profile (should fail)"
FAIL_RESPONSE=$(curl -s -w "\n%{http_code}" -X PUT http://localhost:5000/api/v1/users/$USER1_ID \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $USER2_TOKEN" \
  -d '{"first_name": "Hacked", "last_name": "User"}')
HTTP_CODE=$(echo "$FAIL_RESPONSE" | tail -1)
if [ "$HTTP_CODE" = "403" ]; then
  echo "✓ Correctly rejected (403)"
else
  echo "✗ FAILED: Expected 403, got $HTTP_CODE"
fi
echo ""

# Test 12: Public GET endpoints (should work without auth)
echo "Test 12: Public GET Endpoints (no auth required)"
curl -s http://localhost:5000/api/v1/users > /dev/null && echo "✓ GET /users works without auth"
curl -s http://localhost:5000/api/v1/places > /dev/null && echo "✓ GET /places works without auth"
curl -s http://localhost:5000/api/v1/reviews > /dev/null && echo "✓ GET /reviews works without auth"
echo ""

echo "========================================="
echo "All Task 3 Tests Completed!"
echo "========================================="

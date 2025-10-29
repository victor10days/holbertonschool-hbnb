#!/bin/bash

echo "=== Testing Place API Endpoints ==="
echo

# First create a user and amenities for testing
echo "Setup: Creating user and amenities..."
USER=$(curl -s -X POST http://127.0.0.1:5000/api/v1/users/ \
  -H 'Content-Type: application/json' \
  -d '{"email": "owner@example.com", "first_name": "Owner", "last_name": "User"}')
USER_ID=$(echo "$USER" | python3 -c "import sys, json; print(json.load(sys.stdin)['id'])" 2>/dev/null)

AMENITY1=$(curl -s -X POST http://127.0.0.1:5000/api/v1/amenities/ \
  -H 'Content-Type: application/json' \
  -d '{"name": "WiFi"}')
AMENITY1_ID=$(echo "$AMENITY1" | python3 -c "import sys, json; print(json.load(sys.stdin)['id'])" 2>/dev/null)

AMENITY2=$(curl -s -X POST http://127.0.0.1:5000/api/v1/amenities/ \
  -H 'Content-Type: application/json' \
  -d '{"name": "Pool"}')
AMENITY2_ID=$(echo "$AMENITY2" | python3 -c "import sys, json; print(json.load(sys.stdin)['id'])" 2>/dev/null)

echo "User ID: $USER_ID"
echo "Amenity IDs: $AMENITY1_ID, $AMENITY2_ID"
echo

echo "1. Create place with valid data - Should return 201"
PLACE1=$(curl -s -w "\nHTTP_CODE:%{http_code}" -X POST http://127.0.0.1:5000/api/v1/places/ \
  -H 'Content-Type: application/json' \
  -d "{\"title\": \"Cozy Apartment\", \"description\": \"Nice place\", \"price\": 100.0, \"latitude\": 40.7128, \"longitude\": -74.0060, \"owner_id\": \"$USER_ID\", \"amenities\": [\"$AMENITY1_ID\", \"$AMENITY2_ID\"]}")
echo "$PLACE1" | python3 -m json.tool 2>/dev/null || echo "$PLACE1"
PLACE1_ID=$(echo "$PLACE1" | grep -v "HTTP_CODE" | python3 -c "import sys, json; print(json.load(sys.stdin)['id'])" 2>/dev/null)
echo

echo "2. Create place with negative price - Should return 400"
curl -s -w "\nHTTP_CODE:%{http_code}\n" -X POST http://127.0.0.1:5000/api/v1/places/ \
  -H 'Content-Type: application/json' \
  -d "{\"title\": \"Bad Place\", \"price\": -50.0, \"latitude\": 40.0, \"longitude\": -70.0, \"owner_id\": \"$USER_ID\", \"amenities\": []}"
echo

echo "3. Create place with invalid latitude (>90) - Should return 400"
curl -s -w "\nHTTP_CODE:%{http_code}\n" -X POST http://127.0.0.1:5000/api/v1/places/ \
  -H 'Content-Type: application/json' \
  -d "{\"title\": \"Bad Place\", \"price\": 100.0, \"latitude\": 100.0, \"longitude\": -70.0, \"owner_id\": \"$USER_ID\", \"amenities\": []}"
echo

echo "4. Create place with invalid longitude (<-180) - Should return 400"
curl -s -w "\nHTTP_CODE:%{http_code}\n" -X POST http://127.0.0.1:5000/api/v1/places/ \
  -H 'Content-Type: application/json' \
  -d "{\"title\": \"Bad Place\", \"price\": 100.0, \"latitude\": 40.0, \"longitude\": -200.0, \"owner_id\": \"$USER_ID\", \"amenities\": []}"
echo

echo "5. Create place with non-existent owner - Should return 400"
curl -s -w "\nHTTP_CODE:%{http_code}\n" -X POST http://127.0.0.1:5000/api/v1/places/ \
  -H 'Content-Type: application/json' \
  -d '{"title": "Bad Place", "price": 100.0, "latitude": 40.0, "longitude": -70.0, "owner_id": "invalid-user-id", "amenities": []}'
echo

echo "6. Create place with non-existent amenity - Should return 400"
curl -s -w "\nHTTP_CODE:%{http_code}\n" -X POST http://127.0.0.1:5000/api/v1/places/ \
  -H 'Content-Type: application/json' \
  -d "{\"title\": \"Bad Place\", \"price\": 100.0, \"latitude\": 40.0, \"longitude\": -70.0, \"owner_id\": \"$USER_ID\", \"amenities\": [\"invalid-amenity-id\"]}"
echo

echo "7. Get place by ID with owner and amenities - Should return 200"
curl -s http://127.0.0.1:5000/api/v1/places/$PLACE1_ID | python3 -m json.tool
echo "HTTP_CODE:200"
echo

echo "8. Get place with invalid ID - Should return 404"
curl -s -w "\nHTTP_CODE:%{http_code}\n" http://127.0.0.1:5000/api/v1/places/invalid-place-id
echo

echo "9. Get list of all places - Should return 200"
curl -s http://127.0.0.1:5000/api/v1/places/ | python3 -m json.tool | head -30
echo "HTTP_CODE:200"
echo

echo "10. Update place with valid data - Should return 200"
curl -s -w "\nHTTP_CODE:%{http_code}\n" -X PUT http://127.0.0.1:5000/api/v1/places/$PLACE1_ID \
  -H 'Content-Type: application/json' \
  -d '{"title": "Updated Apartment", "price": 150.0}' | python3 -m json.tool
echo

echo "11. Update place with negative price - Should return 400"
curl -s -w "\nHTTP_CODE:%{http_code}\n" -X PUT http://127.0.0.1:5000/api/v1/places/$PLACE1_ID \
  -H 'Content-Type: application/json' \
  -d '{"price": -100.0}'
echo

echo "12. Update place with invalid latitude - Should return 400"
curl -s -w "\nHTTP_CODE:%{http_code}\n" -X PUT http://127.0.0.1:5000/api/v1/places/$PLACE1_ID \
  -H 'Content-Type: application/json' \
  -d '{"latitude": 95.0}'
echo

echo "13. Update place with invalid ID - Should return 404"
curl -s -w "\nHTTP_CODE:%{http_code}\n" -X PUT http://127.0.0.1:5000/api/v1/places/nonexistent-id \
  -H 'Content-Type: application/json' \
  -d '{"title": "Test"}'
echo

echo "=== All Place tests completed ==="

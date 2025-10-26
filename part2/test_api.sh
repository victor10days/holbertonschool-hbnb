#!/bin/bash
# Quick API test script

echo "========================================="
echo "HBnB API Test Script"
echo "========================================="
echo ""

BASE_URL="http://localhost:5000/api/v1"

echo "1. Creating a user..."
USER_RESPONSE=$(curl -s -X POST $BASE_URL/users \
  -H 'Content-Type: application/json' \
  -d '{"email":"test@example.com","password":"secret123","first_name":"John","last_name":"Doe"}')
echo $USER_RESPONSE | python3 -m json.tool
USER_ID=$(echo $USER_RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin)['id'])")
echo "User ID: $USER_ID"
echo ""

echo "2. Creating an amenity..."
AMENITY_RESPONSE=$(curl -s -X POST $BASE_URL/amenities \
  -H 'Content-Type: application/json' \
  -d '{"name":"WiFi"}')
echo $AMENITY_RESPONSE | python3 -m json.tool
AMENITY_ID=$(echo $AMENITY_RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin)['id'])")
echo "Amenity ID: $AMENITY_ID"
echo ""

echo "3. Creating a place..."
PLACE_RESPONSE=$(curl -s -X POST $BASE_URL/places \
  -H 'Content-Type: application/json' \
  -d "{\"name\":\"Cozy Loft\",\"description\":\"Beautiful apartment\",\"price\":100.0,\"latitude\":40.7128,\"longitude\":-74.0060,\"owner_id\":\"$USER_ID\",\"amenity_ids\":[\"$AMENITY_ID\"]}")
echo $PLACE_RESPONSE | python3 -m json.tool
PLACE_ID=$(echo $PLACE_RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin)['id'])")
echo "Place ID: $PLACE_ID"
echo ""

echo "4. Getting place details (should include owner and amenities)..."
curl -s $BASE_URL/places/$PLACE_ID | python3 -m json.tool
echo ""

echo "5. Listing all users..."
curl -s $BASE_URL/users | python3 -m json.tool
echo ""

echo "========================================="
echo "Test completed!"
echo "========================================="

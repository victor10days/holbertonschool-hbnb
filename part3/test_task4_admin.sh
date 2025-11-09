#!/bin/bash

# Test script for Task 4: Administrator Access Endpoints
# This script tests all admin-only features and admin bypass capabilities

BASE_URL="http://127.0.0.1:5000/api/v1"

echo "=========================================="
echo "Task 4: Administrator Access Endpoints Test"
echo "=========================================="
echo ""

# Step 1: Create a regular user (this should work before we lock it down, or fail if already locked)
echo "1. Attempting to create a regular user without authentication..."
REGULAR_USER=$(curl -s -X POST "$BASE_URL/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "regular@test.com",
    "password": "password123",
    "first_name": "Regular",
    "last_name": "User"
  }')
echo "$REGULAR_USER"
echo ""

# Step 2: Create an admin user (same as above)
echo "2. Attempting to create an admin user without authentication..."
ADMIN_USER=$(curl -s -X POST "$BASE_URL/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@test.com",
    "password": "adminpass",
    "first_name": "Admin",
    "last_name": "User"
  }')
echo "$ADMIN_USER"
echo ""

# Note: You may need to manually set is_admin=True in your database for the admin user
echo "⚠️  NOTE: Make sure admin@test.com has is_admin=True in the database!"
echo ""

# Step 3: Login as regular user
echo "3. Login as regular user..."
REGULAR_TOKEN=$(curl -s -X POST "$BASE_URL/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "regular@test.com",
    "password": "password123"
  }' | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)

if [ -z "$REGULAR_TOKEN" ]; then
  echo "❌ Failed to login as regular user"
  echo "Response: $(curl -s -X POST "$BASE_URL/auth/login" \
    -H "Content-Type: application/json" \
    -d '{
      "email": "regular@test.com",
      "password": "password123"
    }')"
else
  echo "✅ Regular user token: $REGULAR_TOKEN"
fi
echo ""

# Step 4: Login as admin user
echo "4. Login as admin user..."
ADMIN_TOKEN=$(curl -s -X POST "$BASE_URL/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@test.com",
    "password": "adminpass"
  }' | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)

if [ -z "$ADMIN_TOKEN" ]; then
  echo "❌ Failed to login as admin user"
  echo "Response: $(curl -s -X POST "$BASE_URL/auth/login" \
    -H "Content-Type: application/json" \
    -d '{
      "email": "admin@test.com",
      "password": "adminpass"
    }')"
else
  echo "✅ Admin user token: $ADMIN_TOKEN"
fi
echo ""

# Step 5: Test regular user trying to create a new user (should fail)
echo "5. Test: Regular user trying to create a new user (should fail)..."
RESULT=$(curl -s -w "\nHTTP_CODE:%{http_code}" -X POST "$BASE_URL/users/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $REGULAR_TOKEN" \
  -d '{
    "email": "newuser@test.com",
    "password": "password123",
    "first_name": "New",
    "last_name": "User"
  }')
HTTP_CODE=$(echo "$RESULT" | grep "HTTP_CODE:" | cut -d':' -f2)
BODY=$(echo "$RESULT" | sed '/HTTP_CODE:/d')

if [ "$HTTP_CODE" = "403" ]; then
  echo "✅ PASSED: Regular user cannot create users (HTTP 403)"
else
  echo "❌ FAILED: Expected HTTP 403, got HTTP $HTTP_CODE"
  echo "Response: $BODY"
fi
echo ""

# Step 6: Test admin creating a new user (should succeed)
echo "6. Test: Admin creating a new user (should succeed)..."
RESULT=$(curl -s -w "\nHTTP_CODE:%{http_code}" -X POST "$BASE_URL/users/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -d '{
    "email": "created_by_admin@test.com",
    "password": "password123",
    "first_name": "Created",
    "last_name": "ByAdmin"
  }')
HTTP_CODE=$(echo "$RESULT" | grep "HTTP_CODE:" | cut -d':' -f2)
BODY=$(echo "$RESULT" | sed '/HTTP_CODE:/d')

if [ "$HTTP_CODE" = "201" ]; then
  echo "✅ PASSED: Admin can create users (HTTP 201)"
  NEW_USER_ID=$(echo "$BODY" | grep -o '"id":"[^"]*"' | cut -d'"' -f4)
  echo "   New user ID: $NEW_USER_ID"
else
  echo "❌ FAILED: Expected HTTP 201, got HTTP $HTTP_CODE"
  echo "Response: $BODY"
fi
echo ""

# Step 7: Test regular user trying to create an amenity (should fail)
echo "7. Test: Regular user trying to create an amenity (should fail)..."
RESULT=$(curl -s -w "\nHTTP_CODE:%{http_code}" -X POST "$BASE_URL/amenities/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $REGULAR_TOKEN" \
  -d '{
    "name": "WiFi"
  }')
HTTP_CODE=$(echo "$RESULT" | grep "HTTP_CODE:" | cut -d':' -f2)
BODY=$(echo "$RESULT" | sed '/HTTP_CODE:/d')

if [ "$HTTP_CODE" = "403" ]; then
  echo "✅ PASSED: Regular user cannot create amenities (HTTP 403)"
else
  echo "❌ FAILED: Expected HTTP 403, got HTTP $HTTP_CODE"
  echo "Response: $BODY"
fi
echo ""

# Step 8: Test admin creating an amenity (should succeed)
echo "8. Test: Admin creating an amenity (should succeed)..."
RESULT=$(curl -s -w "\nHTTP_CODE:%{http_code}" -X POST "$BASE_URL/amenities/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -d '{
    "name": "Swimming Pool"
  }')
HTTP_CODE=$(echo "$RESULT" | grep "HTTP_CODE:" | cut -d':' -f2)
BODY=$(echo "$RESULT" | sed '/HTTP_CODE:/d')

if [ "$HTTP_CODE" = "201" ]; then
  echo "✅ PASSED: Admin can create amenities (HTTP 201)"
  AMENITY_ID=$(echo "$BODY" | grep -o '"id":"[^"]*"' | cut -d'"' -f4)
  echo "   New amenity ID: $AMENITY_ID"
else
  echo "❌ FAILED: Expected HTTP 201, got HTTP $HTTP_CODE"
  echo "Response: $BODY"
fi
echo ""

# Step 9: Test admin updating an amenity (should succeed)
echo "9. Test: Admin updating an amenity (should succeed)..."
if [ ! -z "$AMENITY_ID" ]; then
  RESULT=$(curl -s -w "\nHTTP_CODE:%{http_code}" -X PUT "$BASE_URL/amenities/$AMENITY_ID" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $ADMIN_TOKEN" \
    -d '{
      "name": "Olympic Swimming Pool"
    }')
  HTTP_CODE=$(echo "$RESULT" | grep "HTTP_CODE:" | cut -d':' -f2)
  BODY=$(echo "$RESULT" | sed '/HTTP_CODE:/d')

  if [ "$HTTP_CODE" = "200" ]; then
    echo "✅ PASSED: Admin can update amenities (HTTP 200)"
  else
    echo "❌ FAILED: Expected HTTP 200, got HTTP $HTTP_CODE"
    echo "Response: $BODY"
  fi
else
  echo "⚠️  SKIPPED: No amenity ID available"
fi
echo ""

# Step 10: Test admin updating another user's email and password (should succeed)
echo "10. Test: Admin updating another user's email and password (should succeed)..."
if [ ! -z "$NEW_USER_ID" ]; then
  RESULT=$(curl -s -w "\nHTTP_CODE:%{http_code}" -X PUT "$BASE_URL/users/$NEW_USER_ID" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $ADMIN_TOKEN" \
    -d '{
      "email": "updated_by_admin@test.com",
      "password": "newpassword123",
      "first_name": "Updated",
      "last_name": "ByAdmin"
    }')
  HTTP_CODE=$(echo "$RESULT" | grep "HTTP_CODE:" | cut -d':' -f2)
  BODY=$(echo "$RESULT" | sed '/HTTP_CODE:/d')

  if [ "$HTTP_CODE" = "200" ]; then
    echo "✅ PASSED: Admin can update user email and password (HTTP 200)"
  else
    echo "❌ FAILED: Expected HTTP 200, got HTTP $HTTP_CODE"
    echo "Response: $BODY"
  fi
else
  echo "⚠️  SKIPPED: No user ID available"
fi
echo ""

# Step 11: Create a place as regular user
echo "11. Creating a place as regular user..."
PLACE_RESULT=$(curl -s -X POST "$BASE_URL/places/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $REGULAR_TOKEN" \
  -d '{
    "name": "Regular User Place",
    "description": "A test place",
    "price": 100.0,
    "latitude": 40.7128,
    "longitude": -74.0060
  }')
PLACE_ID=$(echo "$PLACE_RESULT" | grep -o '"id":"[^"]*"' | head -1 | cut -d'"' -f4)
echo "Place created with ID: $PLACE_ID"
echo ""

# Step 12: Test admin updating a place owned by another user (should succeed)
echo "12. Test: Admin updating a place owned by another user (should succeed)..."
if [ ! -z "$PLACE_ID" ]; then
  RESULT=$(curl -s -w "\nHTTP_CODE:%{http_code}" -X PUT "$BASE_URL/places/$PLACE_ID" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $ADMIN_TOKEN" \
    -d '{
      "name": "Updated by Admin",
      "description": "Updated description",
      "price": 150.0,
      "latitude": 40.7128,
      "longitude": -74.0060
    }')
  HTTP_CODE=$(echo "$RESULT" | grep "HTTP_CODE:" | cut -d':' -f2)
  BODY=$(echo "$RESULT" | sed '/HTTP_CODE:/d')

  if [ "$HTTP_CODE" = "200" ]; then
    echo "✅ PASSED: Admin can update places owned by others (HTTP 200)"
  else
    echo "❌ FAILED: Expected HTTP 200, got HTTP $HTTP_CODE"
    echo "Response: $BODY"
  fi
else
  echo "⚠️  SKIPPED: No place ID available"
fi
echo ""

echo "=========================================="
echo "Test Summary"
echo "=========================================="
echo "All tests completed. Review the results above."
echo ""
echo "Key features tested:"
echo "  ✓ Admin-only user creation"
echo "  ✓ Admin-only amenity creation/modification"
echo "  ✓ Admin can update any user's email/password"
echo "  ✓ Admin can update places owned by others"
echo "  ✓ Regular users are properly restricted"
echo ""

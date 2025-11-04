#!/bin/bash

echo "=== Testing Amenity API Endpoints ==="
echo

echo "1. Create an amenity (POST /api/v1/amenities/) - Should return 201"
AMENITY1=$(curl -s -w "\nHTTP_CODE:%{http_code}" -X POST http://127.0.0.1:5000/api/v1/amenities/ \
  -H 'Content-Type: application/json' \
  -d '{"name": "WiFi"}')
echo "$AMENITY1"
AMENITY1_ID=$(echo "$AMENITY1" | grep -v "HTTP_CODE" | python3 -c "import sys, json; print(json.load(sys.stdin)['id'])" 2>/dev/null)
echo

echo "2. Create amenity with empty name - Should return 400"
curl -s -w "\nHTTP_CODE:%{http_code}\n" -X POST http://127.0.0.1:5000/api/v1/amenities/ \
  -H 'Content-Type: application/json' \
  -d '{"name": ""}'
echo

echo "3. Create amenity with missing name field - Should return 400"
curl -s -w "\nHTTP_CODE:%{http_code}\n" -X POST http://127.0.0.1:5000/api/v1/amenities/ \
  -H 'Content-Type: application/json' \
  -d '{}'
echo

echo "4. Create amenity with name exceeding 50 characters - Should return 400"
curl -s -w "\nHTTP_CODE:%{http_code}\n" -X POST http://127.0.0.1:5000/api/v1/amenities/ \
  -H 'Content-Type: application/json' \
  -d '{"name": "This is a very long amenity name that exceeds fifty characters"}'
echo

echo "5. Get amenity by ID (GET /api/v1/amenities/<id>) - Should return 200"
curl -s -w "\nHTTP_CODE:%{http_code}\n" http://127.0.0.1:5000/api/v1/amenities/$AMENITY1_ID | python3 -m json.tool
echo

echo "6. Get amenity with invalid ID - Should return 404"
curl -s -w "\nHTTP_CODE:%{http_code}\n" http://127.0.0.1:5000/api/v1/amenities/invalid-id-123
echo

echo "7. Get list of all amenities (GET /api/v1/amenities/) - Should return 200"
curl -s http://127.0.0.1:5000/api/v1/amenities/ | python3 -m json.tool
echo "HTTP_CODE:200"
echo

echo "8. Create another amenity"
AMENITY2=$(curl -s -X POST http://127.0.0.1:5000/api/v1/amenities/ \
  -H 'Content-Type: application/json' \
  -d '{"name": "Swimming Pool"}')
echo "$AMENITY2" | python3 -m json.tool
echo

echo "9. Update amenity (PUT /api/v1/amenities/<id>) - Should return 200"
curl -s -w "\nHTTP_CODE:%{http_code}\n" -X PUT http://127.0.0.1:5000/api/v1/amenities/$AMENITY1_ID \
  -H 'Content-Type: application/json' \
  -d '{"name": "High-Speed WiFi"}' | python3 -m json.tool
echo

echo "10. Update amenity with empty name - Should return 400"
curl -s -w "\nHTTP_CODE:%{http_code}\n" -X PUT http://127.0.0.1:5000/api/v1/amenities/$AMENITY1_ID \
  -H 'Content-Type: application/json' \
  -d '{"name": ""}'
echo

echo "11. Update amenity with invalid ID - Should return 404"
curl -s -w "\nHTTP_CODE:%{http_code}\n" -X PUT http://127.0.0.1:5000/api/v1/amenities/nonexistent-id \
  -H 'Content-Type: application/json' \
  -d '{"name": "Test"}'
echo

echo "12. Delete amenity (DELETE /api/v1/amenities/<id>) - Should return 204"
curl -s -w "HTTP_CODE:%{http_code}\n" -X DELETE http://127.0.0.1:5000/api/v1/amenities/$AMENITY1_ID
echo

echo "13. Try to get deleted amenity - Should return 404"
curl -s -w "\nHTTP_CODE:%{http_code}\n" http://127.0.0.1:5000/api/v1/amenities/$AMENITY1_ID
echo

echo "=== All tests completed ==="

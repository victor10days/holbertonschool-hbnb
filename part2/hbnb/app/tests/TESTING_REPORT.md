# HBnB API Testing Report

## User Endpoint
- Valid creation: 201 Created ✅
- Empty fields: 400 Bad Request, error shown ✅
- Invalid email: 400 Bad Request, error shown ✅

## Place Endpoint
- Valid creation: 201 Created ✅
- Missing title: 400 Bad Request, error shown ✅
- Negative price: 400 Bad Request, error shown ✅
- Out-of-range latitude: 400 Bad Request, error shown ✅

## Review Endpoint
- Valid creation: 201 Created ✅
- Empty text: 400 Bad Request, error shown ✅
- Invalid user_id/place_id: 400 Bad Request, error shown ✅

## Swagger Documentation
- [x] All endpoints and fields visible in Swagger UI
- [x] All parameters and responses correctly described

## Automated Unit Tests
- [x] Created and ran unittests for User, Place, Review, Amenity
- [x] All test cases (valid and invalid) pass

**All endpoints validated. Error handling and edge cases confirmed.**

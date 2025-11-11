-- HBnB CRUD Operations Test
-- This script tests Create, Read, Update, and Delete operations

-- ============================================
-- CREATE Operations
-- ============================================

-- Create a test user
INSERT INTO users (id, email, password, first_name, last_name, is_admin, created_at, updated_at)
VALUES (
    'u1111111-1111-1111-1111-111111111111',
    'test@example.com',
    '$2b$12$hashed_password_here',
    'John',
    'Doe',
    FALSE,
    NOW(),
    NOW()
);

-- Create a test place
INSERT INTO places (id, name, description, price, latitude, longitude, owner_id, created_at, updated_at)
VALUES (
    'p1111111-1111-1111-1111-111111111111',
    'Cozy Apartment',
    'A beautiful apartment in the city center',
    100.00,
    40.7128,
    -74.0060,
    'u1111111-1111-1111-1111-111111111111',
    NOW(),
    NOW()
);

-- Associate amenities with the place
INSERT INTO place_amenity (place_id, amenity_id) VALUES
('p1111111-1111-1111-1111-111111111111', 'a1111111-1111-1111-1111-111111111111'),
('p1111111-1111-1111-1111-111111111111', 'a3333333-3333-3333-3333-333333333333'),
('p1111111-1111-1111-1111-111111111111', 'a4444444-4444-4444-4444-444444444444');

-- Create a test review
INSERT INTO reviews (id, text, user_id, place_id, rating, created_at, updated_at)
VALUES (
    'r1111111-1111-1111-1111-111111111111',
    'Great place to stay! Very clean and comfortable.',
    'u1111111-1111-1111-1111-111111111111',
    'p1111111-1111-1111-1111-111111111111',
    5,
    NOW(),
    NOW()
);

-- ============================================
-- READ Operations
-- ============================================

-- Read all users
SELECT 'All Users:' AS query_description;
SELECT id, email, first_name, last_name, is_admin FROM users;

-- Read all amenities
SELECT 'All Amenities:' AS query_description;
SELECT id, name FROM amenities;

-- Read all places with owner information
SELECT 'All Places with Owner Info:' AS query_description;
SELECT
    p.id,
    p.name,
    p.price,
    u.first_name AS owner_first_name,
    u.last_name AS owner_last_name
FROM places p
JOIN users u ON p.owner_id = u.id;

-- Read place with its amenities
SELECT 'Place with Amenities:' AS query_description;
SELECT
    p.name AS place_name,
    a.name AS amenity_name
FROM places p
JOIN place_amenity pa ON p.id = pa.place_id
JOIN amenities a ON pa.amenity_id = a.id
WHERE p.id = 'p1111111-1111-1111-1111-111111111111';

-- Read reviews with user and place information
SELECT 'Reviews with User and Place Info:' AS query_description;
SELECT
    r.text,
    r.rating,
    u.first_name AS reviewer_name,
    p.name AS place_name
FROM reviews r
JOIN users u ON r.user_id = u.id
JOIN places p ON r.place_id = p.id;

-- ============================================
-- UPDATE Operations
-- ============================================

-- Update user information
UPDATE users
SET first_name = 'Jane', last_name = 'Smith', updated_at = NOW()
WHERE id = 'u1111111-1111-1111-1111-111111111111';

-- Verify update
SELECT 'Updated User:' AS query_description;
SELECT id, first_name, last_name FROM users
WHERE id = 'u1111111-1111-1111-1111-111111111111';

-- Update place price
UPDATE places
SET price = 120.00, updated_at = NOW()
WHERE id = 'p1111111-1111-1111-1111-111111111111';

-- Verify update
SELECT 'Updated Place:' AS query_description;
SELECT id, name, price FROM places
WHERE id = 'p1111111-1111-1111-1111-111111111111';

-- Update review rating
UPDATE reviews
SET rating = 4, text = 'Good place, but could be better.', updated_at = NOW()
WHERE id = 'r1111111-1111-1111-1111-111111111111';

-- Verify update
SELECT 'Updated Review:' AS query_description;
SELECT id, text, rating FROM reviews
WHERE id = 'r1111111-1111-1111-1111-111111111111';

-- ============================================
-- DELETE Operations
-- ============================================

-- Delete a review
DELETE FROM reviews WHERE id = 'r1111111-1111-1111-1111-111111111111';

-- Verify deletion
SELECT 'Remaining Reviews:' AS query_description;
SELECT COUNT(*) AS review_count FROM reviews
WHERE id = 'r1111111-1111-1111-1111-111111111111';

-- Delete place (this will cascade delete place_amenity associations)
DELETE FROM places WHERE id = 'p1111111-1111-1111-1111-111111111111';

-- Verify deletion
SELECT 'Remaining Places:' AS query_description;
SELECT COUNT(*) AS place_count FROM places
WHERE id = 'p1111111-1111-1111-1111-111111111111';

-- Verify cascade deletion from place_amenity
SELECT 'Place-Amenity Associations for deleted place:' AS query_description;
SELECT COUNT(*) AS association_count FROM place_amenity
WHERE place_id = 'p1111111-1111-1111-1111-111111111111';

-- Delete test user
DELETE FROM users WHERE id = 'u1111111-1111-1111-1111-111111111111';

-- Final verification
SELECT 'Final User Count:' AS query_description;
SELECT COUNT(*) AS user_count FROM users
WHERE id = 'u1111111-1111-1111-1111-111111111111';

-- ============================================
-- Summary
-- ============================================

SELECT 'CRUD Test Summary:' AS summary;
SELECT 'All CRUD operations completed successfully!' AS result;

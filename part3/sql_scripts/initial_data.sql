-- HBnB Initial Data
-- This script populates the database with initial data

-- Insert administrator user
-- Password is 'admin123' hashed with bcrypt
-- Note: You should update this password hash in production
INSERT INTO users (id, email, password, first_name, last_name, is_admin, created_at, updated_at)
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'admin@hbnb.com',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5gyDh.eYVEH.G',
    'Admin',
    'User',
    TRUE,
    NOW(),
    NOW()
);

-- Insert common amenities
INSERT INTO amenities (id, name, description, created_at, updated_at) VALUES
('a1111111-1111-1111-1111-111111111111', 'WiFi', 'High-speed wireless internet connection', NOW(), NOW()),
('a2222222-2222-2222-2222-222222222222', 'Swimming Pool', 'Outdoor or indoor swimming pool', NOW(), NOW()),
('a3333333-3333-3333-3333-333333333333', 'Air Conditioning', 'Climate control for cooling', NOW(), NOW()),
('a4444444-4444-4444-4444-444444444444', 'Parking', 'Free parking on premises', NOW(), NOW()),
('a5555555-5555-5555-5555-555555555555', 'Kitchen', 'Fully equipped kitchen', NOW(), NOW()),
('a6666666-6666-6666-6666-666666666666', 'TV', 'Television with cable/satellite', NOW(), NOW()),
('a7777777-7777-7777-7777-777777777777', 'Heating', 'Climate control for heating', NOW(), NOW()),
('a8888888-8888-8888-8888-888888888888', 'Washer', 'Washing machine', NOW(), NOW()),
('a9999999-9999-9999-9999-999999999999', 'Dryer', 'Clothes dryer', NOW(), NOW()),
('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 'Gym', 'Fitness center and gym facilities', NOW(), NOW());

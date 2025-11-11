-- HBnB Database Schema
-- This script creates all tables for the HBnB application

-- Drop existing tables (in reverse order of dependencies)
DROP TABLE IF EXISTS place_amenity;
DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS places;
DROP TABLE IF EXISTS amenities;
DROP TABLE IF EXISTS users;

-- Create users table
CREATE TABLE users (
    id VARCHAR(60) PRIMARY KEY,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    email VARCHAR(120) NOT NULL UNIQUE,
    password VARCHAR(128) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    is_admin BOOLEAN NOT NULL DEFAULT FALSE,
    INDEX idx_email (email)
);

-- Create places table
CREATE TABLE places (
    id VARCHAR(60) PRIMARY KEY,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price FLOAT NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    owner_id VARCHAR(60) NOT NULL,
    amenity_ids TEXT NOT NULL DEFAULT '[]',
    FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT chk_price CHECK (price >= 0),
    CONSTRAINT chk_latitude CHECK (latitude >= -90.0 AND latitude <= 90.0),
    CONSTRAINT chk_longitude CHECK (longitude >= -180.0 AND longitude <= 180.0)
);

-- Create reviews table
CREATE TABLE reviews (
    id VARCHAR(60) PRIMARY KEY,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    text TEXT NOT NULL,
    user_id VARCHAR(60) NOT NULL,
    place_id VARCHAR(60) NOT NULL,
    rating INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (place_id) REFERENCES places(id) ON DELETE CASCADE,
    CONSTRAINT chk_rating CHECK (rating >= 0 AND rating <= 5)
);

-- Create amenities table
CREATE TABLE amenities (
    id VARCHAR(60) PRIMARY KEY,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    name VARCHAR(50) NOT NULL
);

-- Create place_amenity association table (many-to-many)
CREATE TABLE place_amenity (
    place_id VARCHAR(60) NOT NULL,
    amenity_id VARCHAR(60) NOT NULL,
    PRIMARY KEY (place_id, amenity_id),
    FOREIGN KEY (place_id) REFERENCES places(id) ON DELETE CASCADE,
    FOREIGN KEY (amenity_id) REFERENCES amenities(id) ON DELETE CASCADE
);

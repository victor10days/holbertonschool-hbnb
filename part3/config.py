"""
Configuration module for the HBnB application.
Contains different configuration classes for various environments.
"""
import os
from datetime import timedelta


class Config:
    """
    Base configuration class.
    Contains default configuration settings.
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = False
    TESTING = False

    # JWT Configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or SECRET_KEY
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)

    # SQLAlchemy Configuration
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False


class DevelopmentConfig(Config):
    """
    Development environment configuration.
    Enables debug mode and other development-specific settings.
    """
    DEBUG = True
    DEVELOPMENT = True

    # SQLite database for development
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///hbnb_dev.db'
    SQLALCHEMY_ECHO = True  # Log SQL queries in development


class TestingConfig(Config):
    """
    Testing environment configuration.
    Used for running tests.
    """
    TESTING = True
    DEBUG = True

    # In-memory SQLite database for testing
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


class ProductionConfig(Config):
    """
    Production environment configuration.
    Should be used in production deployment.
    """
    DEBUG = False

    # MySQL database for production
    # Format: mysql+pymysql://username:password@host:port/database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql+pymysql://hbnb_user:hbnb_pwd@localhost/hbnb_prod'


# Configuration dictionary for easy access
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

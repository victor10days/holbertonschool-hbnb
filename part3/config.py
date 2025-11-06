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


class DevelopmentConfig(Config):
    """
    Development environment configuration.
    Enables debug mode and other development-specific settings.
    """
    DEBUG = True
    DEVELOPMENT = True


class TestingConfig(Config):
    """
    Testing environment configuration.
    Used for running tests.
    """
    TESTING = True
    DEBUG = True


class ProductionConfig(Config):
    """
    Production environment configuration.
    Should be used in production deployment.
    """
    DEBUG = False
    # Additional production-specific settings can be added here


# Configuration dictionary for easy access
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

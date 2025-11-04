"""
Configuration module for the HBnB application.
Contains different configuration classes for various environments.
"""
import os


class Config:
    """
    Base configuration class.
    Contains default configuration settings.
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = False
    TESTING = False


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

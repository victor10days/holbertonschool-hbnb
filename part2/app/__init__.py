from flask import Flask
from flask_restx import Api


def create_app(config_class='config.DevelopmentConfig'):
    """
    Create and configure the Flask application.

    Args:
        config_class: Configuration class to use

    Returns:
        Flask application instance
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask-RESTX API
    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='HBnB Evolution - Part 2: Implementation of business logic and API endpoints',
        doc='/api/v1/docs'
    )

    # Import and register API namespaces
    from app.api.v1 import init_app
    init_app(api)

    return app

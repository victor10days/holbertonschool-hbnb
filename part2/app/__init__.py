from flask import Flask
from flask_restx import Api

def create_app():
    app = Flask(__name__)
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API', doc='/api/v1/')

    # Placeholder for API namespaces (endpoints will be added later)
    # Additional namespaces for places, reviews, and amenities will be added later

    return app

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

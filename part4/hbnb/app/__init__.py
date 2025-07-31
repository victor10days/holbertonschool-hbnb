from flask import Flask
from flask_restx import Api
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key-here'
    
    # Enable CORS for all routes
    CORS(app)
    
    api = Api(app, version='1.0', title='HBnB API', doc='/api/v1/')  # enables Swagger at /api/v1/

    # Import and add your namespaces
    from app.api.v1.users import ns as user_ns
    from app.api.v1.places import ns as place_ns
    from app.api.v1.reviews import ns as review_ns
    from app.api.v1.amenities import ns as amenity_ns
    from app.api.v1.auth import ns as auth_ns
    
    api.add_namespace(user_ns, path='/api/v1/users')
    api.add_namespace(place_ns, path='/api/v1/places')
    api.add_namespace(review_ns, path='/api/v1/reviews')
    api.add_namespace(amenity_ns, path='/api/v1/amenities')
    api.add_namespace(auth_ns, path='/api/v1/auth')

    return app

from flask import Flask, jsonify
from flask_restx import Api
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt

def create_app(config_name='default'):
    app = Flask(__name__)
    
    # Load configuration
    from config import config
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    jwt = JWTManager(app)
    bcrypt = Bcrypt(app)
    
    # JWT Configuration
    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        from app.api.v1.auth import jwt_blacklist
        jti = jwt_payload['jti']
        return jti in jwt_blacklist
    
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return jsonify({'error': 'Token has been revoked'}), 401
    
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({'error': 'Token has expired'}), 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({'error': 'Invalid token'}), 401
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({'error': 'Authentication token is required'}), 401
    
    # Add root route before initializing API
    @app.route('/')
    def index():
        return jsonify({
            'message': 'Welcome to HBnB API',
            'documentation': '/api/v1/',
            'endpoints': {
                'users': '/api/v1/users/',
                'auth': '/api/v1/auth/',
                'places': '/api/v1/places/',
                'reviews': '/api/v1/reviews/',
                'amenities': '/api/v1/amenities/'
            }
        })
    
    # Initialize API with Swagger documentation
    api = Api(app, version='1.0', title='HBnB API', doc='/api/v1/')
    
    # Import and add your namespaces
    from app.api.v1.users import ns as user_ns
    from app.api.v1.auth import ns as auth_ns
    from app.api.v1.places import ns as place_ns
    from app.api.v1.reviews import ns as review_ns
    from app.api.v1.amenities import ns as amenity_ns
    
    api.add_namespace(user_ns, path='/api/v1/users')
    api.add_namespace(auth_ns, path='/api/v1/auth')
    api.add_namespace(place_ns, path='/api/v1/places')
    api.add_namespace(review_ns, path='/api/v1/reviews')
    api.add_namespace(amenity_ns, path='/api/v1/amenities')
    
    return app

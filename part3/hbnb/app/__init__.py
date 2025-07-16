from flask import Flask
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
    
    # Initialize API with Swagger documentation
    api = Api(app, version='1.0', title='HBnB API', doc='/api/v1/')
    
    # Import and add your namespaces
    from app.api.v1.users import ns as user_ns
    api.add_namespace(user_ns, path='/api/v1/users')
    
    # TODO: Add other namespaces (places, reviews, amenities) when created
    
    return app

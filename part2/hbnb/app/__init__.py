from flask import Flask
from flask_restx import Api

def create_app():
    app = Flask(__name__)
    api = Api(app, version='1.0', title='HBnB API', doc='/api/v1/')  # enables Swagger at /api/v1/

    # Import and add your namespaces
    from app.api.v1.users import ns as user_ns
    api.add_namespace(user_ns, path='/api/v1/users')
    # (repeat for other entities, if present)

    return app

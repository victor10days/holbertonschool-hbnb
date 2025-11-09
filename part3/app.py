from flask import Flask
from flask_restx import Api
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from hbnb.errors import register_error_handlers
from hbnb.facade import HbnbFacade
from hbnb.persistence.user_repository import UserRepository
from hbnb.api.v1.users import ns as users_ns
from hbnb.api.v1.amenities import ns as amenities_ns
from hbnb.api.v1.places import ns as places_ns
from hbnb.api.v1.reviews import ns as reviews_ns
from hbnb.api.v1.auth import ns as auth_ns
from hbnb.bl.user import bcrypt
from hbnb.bl.base import Base

# Initialize SQLAlchemy with our custom Base class
db = SQLAlchemy(model_class=Base)

def create_app(config_class="config.DevelopmentConfig") -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    bcrypt.init_app(app)
    jwt = JWTManager(app)
    db.init_app(app)

    # Create database tables
    with app.app_context():
        db.create_all()

        # Initialize UserRepository with database session
        user_repo = UserRepository(db.session)

        # Attach shared facade with the UserRepository
        app.config["FACADE"] = HbnbFacade(repo=user_repo)

    # Initialize API
    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='HBnB Application API',
        doc='/api/v1/docs'
    )

    # register namespaces
    api.add_namespace(users_ns, path="/api/v1/users")
    api.add_namespace(amenities_ns, path="/api/v1/amenities")
    api.add_namespace(places_ns, path="/api/v1/places")
    api.add_namespace(reviews_ns, path="/api/v1/reviews")
    api.add_namespace(auth_ns, path="/api/v1/auth")

    register_error_handlers(app)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)

from flask import Flask
from flask_restx import Api
from hbnb.errors import register_error_handlers
from hbnb.facade import HbnbFacade
from hbnb.api.v1.users import ns as users_ns
from hbnb.api.v1.amenities import ns as amenities_ns
from hbnb.api.v1.places import ns as places_ns
from hbnb.api.v1.reviews import ns as reviews_ns

def create_app() -> Flask:
    app = Flask(__name__)
    api = Api(app, version="1.0", title="HBnB API", description="HBnB v2 — Part 2")

    # attach shared facade
    app.config["FACADE"] = HbnbFacade()

    # register namespaces
    api.add_namespace(users_ns, path="/api/v1/users")
    api.add_namespace(amenities_ns, path="/api/v1/amenities")
    api.add_namespace(places_ns, path="/api/v1/places")
    api.add_namespace(reviews_ns, path="/api/v1/reviews")

    register_error_handlers(app)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)

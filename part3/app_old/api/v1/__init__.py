def init_app(api):
    """Initialize API namespaces"""
    # Import namespaces from endpoint modules
    from app.api.v1.users import users_ns
    from app.api.v1.places import places_ns
    from app.api.v1.reviews import reviews_ns
    from app.api.v1.amenities import amenities_ns

    # Register namespaces
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')

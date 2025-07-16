class HBnBFacade:
    """
    Facade for the HBnB application, providing a simplified interface to the underlying business logic.
    """

    def __init__(self, hbnb_service):
        self.hbnb_service = hbnb_service

    def create_user(self, user_data):
        return self.hbnb_service.create_user(user_data)

    def get_user(self, user_id):
        return self.hbnb_service.get_user(user_id)

    def create_listing(self, listing_data):
        return self.hbnb_service.create_listing(listing_data)

    def get_listing(self, listing_id):
        return self.hbnb_service.get_listing(listing_id)

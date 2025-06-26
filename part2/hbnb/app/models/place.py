from .base_model import BaseModel

class Place(BaseModel):
    def __init__(self, title, price, latitude, longitude, **kwargs):
        if not title:
            raise ValueError("title is required")
        if not isinstance(price, (int, float)) or price <= 0:
            raise ValueError("price must be a positive number")
        if not (-90 <= latitude <= 90):
            raise ValueError("latitude must be between -90 and 90")
        if not (-180 <= longitude <= 180):
            raise ValueError("longitude must be between -180 and 180")
        super().__init__()
        self.title = title
        self.price = price
        self.latitude = latitude
        self.longitude = longitude

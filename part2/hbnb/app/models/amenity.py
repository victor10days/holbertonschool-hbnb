class Amenity:
    def __init__(self, name: str, description: str, location: str):
        self.name = name
        self.description = description
        self.location = location

    def __str__(self):
        return f"Amenity(name={self.name}, description={self.description}, location={self.location})"

    def __repr__(self):
        return self.__str__()

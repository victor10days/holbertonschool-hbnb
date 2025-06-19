class Place:
    def __init__(self, name: str, address: str):
        self.name = name
        self.address = address

    def __str__(self):
        return f"{self.name} located at {self.address}"

    def __repr__(self):
        return f"Place(name={self.name}, address={self.address})"

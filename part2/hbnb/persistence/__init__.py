"""
Persistence layer package
"""
from hbnb.persistence.memory_repo import MemoryRepository

# Create singleton instance
repository = MemoryRepository()

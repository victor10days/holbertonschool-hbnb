"""
Persistence layer package
"""
from hbnb.persistence.memory_repo import MemoryRepository
from hbnb.persistence.sqlalchemy_repo import SQLAlchemyRepository

# Create singleton instance
repository = MemoryRepository()

__all__ = ['MemoryRepository', 'SQLAlchemyRepository', 'repository']

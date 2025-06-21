# hbnb/app/persistence/repository.py

class Repository:
    def __init__(self):
        self._objects = {}

    def add(self, obj):
        self._objects[obj.id] = obj

    def get(self, obj_id):
        return self._objects.get(obj_id)

    def get_all(self):
        return list(self._objects.values())

    def update(self, obj_id, **kwargs):
        obj = self.get(obj_id)
        if not obj:
            return None
        for key, value in kwargs.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(obj, key, value)
        obj.save()
        return obj

    def delete(self, obj_id):
        if obj_id in self._objects:
            del self._objects[obj_id]
            return True
        return False

# Hold repositories for each type as a singleton
_repos = {}

def get_repository(kind):
    if kind not in _repos:
        _repos[kind] = Repository()
    return _repos[kind]

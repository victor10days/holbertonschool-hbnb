from typing import Tuple

def paginate(items, page: int, per_page: int) -> Tuple[list, int]:
    total = len(items)
    start = (page - 1) * per_page
    end = start + per_page
    return items[start:end], total

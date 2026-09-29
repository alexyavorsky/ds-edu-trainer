from collections import OrderedDict


class PreviewCache:
    """Кэш на capacity элементов с вытеснением давно не использованных (LRU)."""

    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self.items: OrderedDict[str, str] = OrderedDict()

    def get(self, photo_id: str) -> str | None:
        if photo_id not in self.items:
            return None
        self.items.move_to_end(photo_id)
        return self.items[photo_id]

    def put(self, photo_id: str, preview: str) -> None:
        self.items[photo_id] = preview
        self.items.move_to_end(photo_id)
        if len(self.items) > self.capacity:
            self.items.popitem(last=False)

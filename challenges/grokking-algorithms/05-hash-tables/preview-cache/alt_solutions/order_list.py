class PreviewCache:
    """Кэш на capacity элементов с вытеснением давно не использованных (LRU)."""

    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self.data: dict[str, str] = {}
        self.order: list[str] = []  # от давнего к недавнему; удаление из списка — O(capacity), но верно

    def get(self, photo_id: str) -> str | None:
        if photo_id not in self.data:
            return None
        self.order.remove(photo_id)
        self.order.append(photo_id)
        return self.data[photo_id]

    def put(self, photo_id: str, preview: str) -> None:
        if photo_id in self.data:
            self.order.remove(photo_id)
        elif len(self.data) == self.capacity:
            oldest = self.order.pop(0)
            del self.data[oldest]
        self.data[photo_id] = preview
        self.order.append(photo_id)

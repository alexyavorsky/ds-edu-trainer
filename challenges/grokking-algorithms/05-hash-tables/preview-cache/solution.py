class PreviewCache:
    """Кэш на capacity элементов с вытеснением давно не использованных (LRU)."""

    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self.data: dict[str, str] = {}  # порядок ключей: от давно использованных к недавним

    def _touch(self, photo_id: str) -> None:
        self.data[photo_id] = self.data.pop(photo_id)  # переносим в конец

    def get(self, photo_id: str) -> str | None:
        if photo_id not in self.data:
            return None
        self._touch(photo_id)
        return self.data[photo_id]

    def put(self, photo_id: str, preview: str) -> None:
        if photo_id in self.data:
            self._touch(photo_id)
        elif len(self.data) >= self.capacity:
            del self.data[next(iter(self.data))]  # вытесняем самый давний
        self.data[photo_id] = preview

class PreviewCache:
    """Кэш на capacity элементов с вытеснением давно не использованных (LRU)."""

    def __init__(self, capacity: int) -> None:
        # ваш код
        raise NotImplementedError

    def get(self, photo_id: str) -> str | None:
        # ваш код
        raise NotImplementedError

    def put(self, photo_id: str, preview: str) -> None:
        # ваш код
        raise NotImplementedError

class ChainedHashTable:
    """Хеш-таблица с разрешением коллизий цепочками."""

    def __init__(self, size: int = 8) -> None:
        self.buckets: list[list[tuple[str, int]]] = [[] for _ in range(size)]

    def _bucket(self, key: str) -> list[tuple[str, int]]:
        return self.buckets[hash(key) % len(self.buckets)]

    def put(self, key: str, value: int) -> None:
        """Добавляет пару или обновляет значение существующего ключа."""
        bucket = self._bucket(key)
        for i, (k, _) in enumerate(bucket):
            # TODO: если ключ уже есть — замените пару и выйдите из метода
            pass
        # TODO: ключа не было — добавьте пару в корзину

    def get(self, key: str, default: int | None = None) -> int | None:
        """Значение по ключу или default."""
        # TODO: найдите ключ в его корзине
        return default

    def __len__(self) -> int:
        return sum(len(bucket) for bucket in self.buckets)

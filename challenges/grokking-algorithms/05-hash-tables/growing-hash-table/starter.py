class GrowingHashTable:
    """Хеш-таблица с цепочками, удваивается при коэффициенте заполнения > 0.7."""

    def __init__(self) -> None:
        self.buckets: list[list[tuple[object, object]]] = [[] for _ in range(4)]
        self.count = 0

    def load_factor(self) -> float:
        return self.count // len(self.buckets)

    def put(self, key: object, value: object) -> None:
        bucket = self.buckets[hash(key) % len(self.buckets)]
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))
        self.count += 1
        if self.load_factor() > 0.7:
            self._resize()

    def _resize(self) -> None:
        old = self.buckets
        self.buckets = [[] for _ in range(len(old) * 2)]
        for i, bucket in enumerate(old):
            self.buckets[i] = bucket

    def get(self, key: object, default: object = None) -> object:
        for k, v in self.buckets[hash(key) % len(self.buckets)]:
            if k == key:
                return v
        return default

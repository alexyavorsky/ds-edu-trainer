class VisitCounter:
    def __init__(self) -> None:
        self._count = 0

    def increment(self) -> None:
        self._count += 1

    def reset(self) -> None:
        self._count = 0

    @property
    def value(self) -> int:
        return self._count

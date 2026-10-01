class VisitCounter:
    def __init__(self) -> None:
        self._visits: list[int] = []

    def increment(self) -> None:
        self._visits.append(1)

    def reset(self) -> None:
        self._visits.clear()

    @property
    def value(self) -> int:
        return len(self._visits)

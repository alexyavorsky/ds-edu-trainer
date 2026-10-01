class VisitCounter:
    def __init__(self) -> None:
        raise NotImplementedError

    def increment(self) -> None:
        raise NotImplementedError

    def reset(self) -> None:
        raise NotImplementedError

    @property
    def value(self) -> int:
        raise NotImplementedError

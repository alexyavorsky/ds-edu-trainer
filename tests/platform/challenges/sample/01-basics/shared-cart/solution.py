_NO_ITEMS: list[str] = []


class Cart:
    def __init__(self) -> None:
        self.items = list(_NO_ITEMS)

    def add(self, item: str) -> None:
        self.items.append(item)

    def count(self) -> int:
        return len(self.items)

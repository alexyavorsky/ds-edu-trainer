class _Budget(list):
    """Список с бюджетом чтений: медленное решение падает сразу, а не зависает."""

    def __init__(self, data, limit: int) -> None:
        super().__init__(data)
        self.limit = limit
        self.reads = 0

    def _spend(self, n: int) -> None:
        self.reads += n
        if self.reads > self.limit:
            raise AssertionError(f"прочитано больше {self.limit} элементов (лимит — 3 прохода по списку) — похоже на перебор пар")

    def __getitem__(self, i):
        value = super().__getitem__(i)
        self._spend(len(value) if isinstance(i, slice) else 1)
        return value

    def __iter__(self):
        self._spend(len(self))
        return super().__iter__()

    def __contains__(self, x):
        self._spend(len(self))
        return super().__contains__(x)

    def index(self, *args):
        self._spend(len(self))
        return super().index(*args)

    def count(self, x):
        self._spend(len(self))
        return super().count(x)


def _check_pair(prices: list[int], total: int, got) -> None:
    assert isinstance(got, tuple) and len(got) == 2, f"ожидалась пара индексов, получено {got!r}"
    i, j = got
    assert 0 <= i < j < len(prices), f"индексы должны быть 0 <= i < j < {len(prices)}, получено {got!r}"
    assert prices[i] + prices[j] == total, f"{prices[i]} + {prices[j]} ≠ {total}"


def test_example():
    """Пример: 300 + 1200 = 1500"""
    prices = [700, 1500, 300, 1200]
    _check_pair(prices, 1500, pair_for_card(prices, 1500))


def test_same_price_twice():
    """Два разных товара с одинаковой ценой"""
    _check_pair([500, 500], 1000, pair_for_card([500, 500], 1000))


def test_single_item_not_twice():
    """Один товар нельзя взять дважды → None"""
    got = pair_for_card([500], 1000)
    assert got is None, f"ожидалось None, получено {got!r}"


def test_no_pair():
    """Подходящей пары нет → None"""
    got = pair_for_card([100, 200, 400], 1000)
    assert got is None, f"ожидалось None, получено {got!r}"


def test_empty():
    """Пустой список → None"""
    got = pair_for_card([], 10)
    assert got is None, f"ожидалось None, получено {got!r}"


def test_zero_and_negative():
    """Нулевая цена (бесплатный товар) и total = 0"""
    _check_pair([0, 5, 0], 0, pair_for_card([0, 5, 0], 0))
    _check_pair([3, 0, 9], 9, pair_for_card([3, 0, 9], 9))


def test_several_pairs():
    """Несколько подходящих пар — годится любая"""
    prices = [1, 9, 2, 8, 3, 7]
    _check_pair(prices, 10, pair_for_card(prices, 10))


def test_large():
    """300 000 товаров, пара в самом конце: верная пара, список читается не больше 3 раз"""
    data = list(range(1, 300_001)) + [10**9]
    prices = _Budget(data, limit=3 * len(data))
    got = pair_for_card(prices, 10**9 + 7)
    _check_pair(data, 10**9 + 7, got)

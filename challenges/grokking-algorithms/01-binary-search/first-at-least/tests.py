class _Tracked(list):
    """Список, который считает чтения элементов (срез читает все скопированные элементы)."""

    reads = 0

    def __getitem__(self, i):
        value = super().__getitem__(i)
        self.reads += len(value) if isinstance(i, slice) else 1
        return value

    def __iter__(self):
        self.reads += len(self)
        return super().__iter__()

    def __contains__(self, x):
        self.reads += len(self)
        return super().__contains__(x)

    def index(self, *args):
        self.reads += len(self)
        return super().index(*args)


PRICES = [100, 250, 250, 250, 400]


def test_duplicates_first():
    """Среди одинаковых цен — индекс первой: 250 → 1"""
    got = first_at_least(PRICES, 250)
    assert got == 1, f"ожидалось 1, получено {got!r}"


def test_between():
    """Бюджет между ценами: 260 → 4"""
    got = first_at_least(PRICES, 260)
    assert got == 4, f"ожидалось 4, получено {got!r}"


def test_below_all():
    """Бюджет меньше всех цен → 0"""
    got = first_at_least(PRICES, 50)
    assert got == 0, f"ожидалось 0, получено {got!r}"


def test_above_all():
    """Бюджет больше всех цен → len(prices)"""
    got = first_at_least(PRICES, 500)
    assert got == 5, f"ожидалось 5, получено {got!r}"


def test_empty():
    """Пустой список → 0"""
    got = first_at_least([], 10)
    assert got == 0, f"ожидалось 0, получено {got!r}"


def test_brute_force():
    """Совпадает с полным перебором на разных списках"""
    cases = [[1], [5, 5, 5], [1, 2, 3, 4, 5, 6], [2, 2, 4, 4, 4, 8, 9, 9]]
    for prices in cases:
        for budget in range(0, 11):
            expected = next((i for i, p in enumerate(prices) if p >= budget), len(prices))
            got = first_at_least(prices, budget)
            assert got == expected, f"prices={prices}, budget={budget}: ожидалось {expected}, получено {got!r}"


def test_logarithmic_on_equal():
    """100 000 одинаковых цен: верные ответы и не больше 60 прочитанных элементов"""
    prices = _Tracked([7] * 100_000)
    for budget, expected in [(7, 0), (6, 0), (8, 100_000)]:
        prices.reads = 0
        got = first_at_least(prices, budget)
        assert got == expected, f"бюджет {budget}: ожидалось {expected}, получено {got!r}"
        assert prices.reads <= 60, (
            f"бюджет {budget}: прочитано {prices.reads} элементов при лимите 60 (бинарному поиску хватает ~17) — "
            "похоже на перебор или копирование среза"
        )

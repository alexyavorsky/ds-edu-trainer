class _Budget(list):
    """Список с бюджетом чтений: медленное решение падает сразу, а не зависает."""

    def __init__(self, data, limit: int) -> None:
        super().__init__(data)
        self.limit = limit
        self.reads = 0

    def _spend(self, n: int) -> None:
        self.reads += n
        if self.reads > self.limit:
            raise AssertionError(
                f"прочитано больше {self.limit} элементов (лимит) — похоже на перебор скоростей подряд вместо бинарного поиска"
            )

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


BOOK = [30, 11, 23, 4, 20]


def test_days_needed():
    """days_needed: 23 стр./день → 6 дней, 22 → 7 дней"""
    assert days_needed(BOOK, 23) == 6, f"скорость 23: получено {days_needed(BOOK, 23)!r}"
    assert days_needed(BOOK, 22) == 7, f"скорость 22: получено {days_needed(BOOK, 22)!r}"


def test_days_needed_exact_division():
    """days_needed: главы делятся нацело без лишнего дня"""
    got = days_needed([10, 20, 30], 10)
    assert got == 6, f"ожидалось 6, получено {got!r}"


def test_example():
    """Пример из условия → 23"""
    got = min_daily_pages(BOOK, 6)
    assert got == 23, f"ожидалось 23, получено {got!r}"


def test_one_day_per_chapter():
    """Дней столько же, сколько глав → самая длинная глава"""
    got = min_daily_pages(BOOK, 5)
    assert got == 30, f"ожидалось 30, получено {got!r}"


def test_plenty_of_days():
    """Дней больше, чем страниц → 1 страница в день"""
    got = min_daily_pages(BOOK, 1000)
    assert got == 1, f"ожидалось 1, получено {got!r}"


def test_single_chapter():
    """Одна глава из 10 страниц за 3 дня → 4"""
    got = min_daily_pages([10], 3)
    assert got == 4, f"ожидалось 4, получено {got!r}"


def test_minimal():
    """Ответ минимален: со скоростью на 1 меньше не успеть"""
    cases = [([7, 1, 9, 2, 8], 9), ([100, 100], 7), ([1, 1, 1, 50], 10), ([5, 5, 5, 5], 4)]
    for chapters, days in cases:
        s = min_daily_pages(chapters, days)
        assert days_needed(chapters, s) <= days, f"{chapters}, {days} дн.: со скоростью {s} не успеть"
        assert s == 1 or days_needed(chapters, s - 1) > days, f"{chapters}, {days} дн.: {s - 1} тоже хватает"


def test_huge():
    """10⁵ глав по 10⁹ страниц: верный ответ и не больше 100 проходов по списку глав"""
    chapters = _Budget([10**9] * 100_000, limit=100 * 100_000)
    got = min_daily_pages(chapters, 300_000)
    assert got == 333_333_334, f"ожидалось 333333334, получено {got!r}"

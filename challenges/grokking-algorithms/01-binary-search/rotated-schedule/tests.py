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


TIMES = [900, 1020, 1300, 15, 240, 600]


def test_example():
    """Пример из условия: 240 → 4, 1020 → 1"""
    assert find_departure(TIMES, 240) == 4, f"240: получено {find_departure(TIMES, 240)!r}"
    assert find_departure(TIMES, 1020) == 1, f"1020: получено {find_departure(TIMES, 1020)!r}"


def test_not_found():
    """Отсутствующее время → -1"""
    for target in (700, 0, 1439, 16):
        got = find_departure(TIMES, target)
        assert got == -1, f"{target}: ожидалось -1, получено {got!r}"


def test_empty():
    """Пустое расписание → -1"""
    got = find_departure([], 10)
    assert got == -1, f"ожидалось -1, получено {got!r}"


def test_single():
    """Одно отправление"""
    assert find_departure([42], 42) == 0, "не найдено единственное отправление"
    assert find_departure([42], 41) == -1, "найдено несуществующее отправление"


def test_not_rotated():
    """Список без сдвига"""
    times = [10, 20, 30, 40, 50]
    for i, t in enumerate(times):
        got = find_departure(times, t)
        assert got == i, f"{t}: ожидалось {i}, получено {got!r}"


def test_all_rotations():
    """Все сдвиги списка из 9 элементов, все значения и промахи"""
    base = [3, 8, 15, 16, 23, 42, 50, 61, 77]
    for shift in range(len(base)):
        times = base[shift:] + base[:shift]
        for i, t in enumerate(times):
            got = find_departure(times, t)
            assert got == i, f"сдвиг {shift}, target {t}: ожидалось {i}, получено {got!r}"
        for miss in (0, 9, 30, 100):
            got = find_departure(times, miss)
            assert got == -1, f"сдвиг {shift}, target {miss}: ожидалось -1, получено {got!r}"


def test_logarithmic():
    """100 000 элементов: верные ответы и не больше 150 прочитанных элементов на поиск"""
    base = list(range(0, 300_000, 3))
    times = _Tracked(base[61_803:] + base[:61_803])
    for target in (0, 3 * 61_803, 3 * 99_999, 3 * 30_000, 1):
        times.reads = 0
        got = find_departure(times, target)
        expected = (target // 3 - 61_803) % 100_000 if target % 3 == 0 else -1
        assert got == expected, f"target {target}: ожидалось {expected}, получено {got!r}"
        assert times.reads <= 150, (
            f"target {target}: прочитано {times.reads} элементов при лимите 150 (бинарному поиску хватает ~50) — "
            "похоже на перебор или копирование среза"
        )

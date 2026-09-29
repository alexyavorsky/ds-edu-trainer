class _Budget(list):
    """Список с бюджетом чтений: медленное решение падает сразу, а не зависает."""

    def __init__(self, data, limit: int) -> None:
        super().__init__(data)
        self.limit = limit
        self.reads = 0

    def _spend(self, n: int) -> None:
        self.reads += n
        if self.reads > self.limit:
            raise AssertionError(f"журнал прочитан больше {self.limit // len(self)} раз (лимит) — похоже на повторные проходы по списку")

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


def test_example():
    """Пример: повтор B7 раньше повтора A1"""
    got = first_repeat(["A1", "B7", "C3", "B7", "A1"])
    assert got == "B7", f"ожидалось 'B7', получено {got!r}"


def test_no_repeats():
    """Без повторов → None"""
    got = first_repeat(["A1", "B7", "C3"])
    assert got is None, f"ожидалось None, получено {got!r}"


def test_empty():
    """Пустой журнал → None"""
    got = first_repeat([])
    assert got is None, f"ожидалось None, получено {got!r}"


def test_single():
    """Один проход → None"""
    got = first_repeat(["Z9"])
    assert got is None, f"ожидалось None, получено {got!r}"


def test_immediate_repeat():
    """Повтор подряд"""
    got = first_repeat(["X", "X"])
    assert got == "X", f"ожидалось 'X', получено {got!r}"


def test_first_seen_is_not_answer():
    """Ответ — по моменту второго прохода, а не первого"""
    got = first_repeat(["A", "B", "C", "C", "B", "A"])
    assert got == "C", f"ожидалось 'C', получено {got!r}"


def test_many_scans():
    """50 000 проходов: верный ответ, журнал читается не больше 3 раз"""
    data = [f"T{i}" for i in range(50_000)] + ["T12345", "T5"]
    scans = _Budget(data, limit=3 * len(data))
    got = first_repeat(scans)
    assert got == "T12345", f"ожидалось 'T12345', получено {got!r}"


test_many_scans.timeout = 3
test_many_scans.timeout_hint = "Если «уже виденные» хранятся в списке, каждая проверка просматривает его целиком — используйте set"

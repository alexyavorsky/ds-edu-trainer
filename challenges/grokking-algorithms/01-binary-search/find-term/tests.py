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


TERMS = ["алгоритм", "граф", "массив", "очередь", "стек"]


def test_found_middle():
    """Термин в середине: «массив» → 2"""
    got = find_term(TERMS, "массив")
    assert got == 2, f"ожидалось 2, получено {got!r}"


def test_found_edges():
    """Первый и последний термины находятся"""
    got = find_term(TERMS, "алгоритм")
    assert got == 0, f"«алгоритм»: ожидалось 0, получено {got!r}"
    got = find_term(TERMS, "стек")
    assert got == 4, f"«стек»: ожидалось 4, получено {got!r}"


def test_every_term():
    """Каждый термин находится на своём месте (списки длины 1–8)"""
    for n in range(1, 9):
        terms = TERMS[:n] if n <= len(TERMS) else TERMS + ["ф" * k for k in range(1, n - len(TERMS) + 1)]
        for i, term in enumerate(terms):
            got = find_term(terms, term)
            assert got == i, f"список из {n}: «{term}» ожидался на месте {i}, получено {got!r}"


def test_not_found():
    """Отсутствующий термин → None: раньше всех, между соседями и позже всех"""
    for term in ["абак", "дерево", "явление"]:
        got = find_term(TERMS, term)
        assert got is None, f"«{term}»: ожидалось None, получено {got!r}"


def test_empty():
    """Пустой глоссарий → None"""
    got = find_term([], "граф")
    assert got is None, f"ожидалось None, получено {got!r}"


def test_single():
    """Глоссарий из одного термина: находится и не находится"""
    got = find_term(["граф"], "граф")
    assert got == 0, f"find_term(['граф'], 'граф'): ожидалось 0, получено {got!r}"
    got = find_term(["граф"], "стек")
    assert got is None, f"find_term(['граф'], 'стек'): ожидалось None, получено {got!r}"


def test_logarithmic():
    """100 000 терминов: верные ответы и не больше 60 прочитанных элементов на поиск"""
    terms = _Tracked(f"термин-{i:06d}" for i in range(100_000))
    cases = [
        ("термин-000000", 0),
        ("термин-071234", 71234),
        ("термин-099999", 99999),
        ("термин-5", None),
        ("абак", None),
        ("яблоко", None),
    ]
    for target, expected in cases:
        terms.reads = 0
        got = find_term(terms, target)
        assert got == expected, f"«{target}»: ожидалось {expected!r}, получено {got!r}"
        assert terms.reads <= 60, (
            f"«{target}»: прочитано {terms.reads} элементов при лимите 60 (бинарному поиску хватает ~17) — "
            "похоже на перебор или копирование среза (срез копирует элементы)"
        )

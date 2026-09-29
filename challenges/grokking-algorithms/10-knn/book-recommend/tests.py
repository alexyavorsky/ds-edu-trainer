RATINGS = {
    "Аня": {"Дюна": 5, "Солярис": 4, "Пикник": 1},
    "Боря": {"Дюна": 5, "Солярис": 5, "Гиперион": 4},
    "Вика": {"Дюна": 1, "Пикник": 5, "Мастер": 5},
    "Гоша": {"Солярис": 4, "Гиперион": 2, "Мастер": 3},
}


def test_example():
    """Пример из условия"""
    got = recommend(RATINGS, "Аня", 2)
    assert got == ["Гиперион", "Мастер"], f"получено {got!r}"


def test_k_one():
    """k = 1: сосед — Гоша (одна общая книга даёт сходство 1.0, у Бори ≈ 0.994)"""
    got = recommend(RATINGS, "Аня", 1)
    assert got == ["Мастер", "Гиперион"], f"получено {got!r} (оценки Гоши: Мастер 3, Гиперион 2)"


def test_average_and_order():
    """Средняя оценка по соседям, сортировка по убыванию"""
    ratings = {
        "u": {"a": 5},
        "n1": {"a": 5, "x": 4, "y": 2},
        "n2": {"a": 4, "x": 2, "z": 5},
    }
    got = recommend(ratings, "u", 2)
    assert got == ["z", "x", "y"], f"получено {got!r} (оценки: z 5, x 3, y 2)"


def test_alphabetical_tie():
    """Равные оценки — по алфавиту"""
    ratings = {"u": {"a": 3}, "n": {"a": 3, "в": 4, "б": 4}}
    got = recommend(ratings, "u", 1)
    assert got == ["б", "в"], f"получено {got!r}"


def test_zero_similarity_ignored():
    """Читатели без общих книг — не соседи"""
    ratings = {"u": {"a": 5}, "stranger": {"b": 5, "c": 5}}
    got = recommend(ratings, "u", 3)
    assert got == [], f"ожидалось [], получено {got!r}"


def test_neighbor_tie_by_name():
    """Равное сходство — сосед с меньшим именем"""
    ratings = {"u": {"a": 4}, "Яна": {"a": 2, "y": 5}, "Ада": {"a": 1, "x": 5}}
    got = recommend(ratings, "u", 1)
    assert got == ["x"], f"получено {got!r} — у обоих сходство 1.0, выбирается Ада"


def test_unknown_user_and_nothing_new():
    """Неизвестный читатель и нечего рекомендовать → []"""
    assert recommend(RATINGS, "Никто", 2) == [], "неизвестный читатель"
    ratings = {"u": {"a": 5, "b": 3}, "v": {"a": 4, "b": 4}}
    assert recommend(ratings, "u", 1) == [], "все книги соседа уже прочитаны"

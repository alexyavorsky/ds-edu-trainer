CANDIDATES = {
    "Ира": {"python", "ml", "sql"},
    "Кирилл": {"devops", "python"},
    "Лена": {"design", "sql"},
    "Миша": {"ml"},
}


def _check(needed, candidates, max_size):
    team = pick_team(needed, candidates)
    assert isinstance(team, list), f"ожидался список имён, получено {team!r}"
    assert all(name in candidates for name in team), f"в команде есть неизвестные имена: {team}"
    assert len(set(team)) == len(team), f"кандидат взят дважды: {team}"
    covered = set().union(*(candidates[n] for n in team)) if team else set()
    missing = needed - covered
    assert not missing, f"не покрыты навыки {missing}: команда {team}"
    assert len(team) <= max_size, f"в команде {len(team)} человек, жадный алгоритм обходится {max_size}: {team}"


def test_example():
    """Пример из условия: хватает трёх человек"""
    _check({"python", "sql", "ml", "devops", "design"}, CANDIDATES, 3)


def test_nothing_needed():
    """Ничего не нужно → пустая команда"""
    got = pick_team(set(), CANDIDATES)
    assert got == [], f"ожидалось [], получено {got!r}"


def test_impossible():
    """Навыка нет ни у кого → None"""
    got = pick_team({"python", "rust"}, CANDIDATES)
    assert got is None, f"ожидалось None, получено {got!r}"


def test_one_covers_all():
    """Один кандидат знает всё — берётся он один"""
    candidates = {**CANDIDATES, "Олег": {"python", "sql", "ml", "devops", "design"}}
    _check({"python", "sql", "ml", "devops", "design"}, candidates, 1)


def test_ignores_useless():
    """Кандидаты без нужных навыков не берутся"""
    candidates = {"a": {"x"}, "b": {"y"}, "c": {"z", "q"}}
    team = pick_team({"x", "y"}, candidates)
    assert team is not None and "c" not in team, f"c ничего не добавляет, но взят: {team}"
    _check({"x", "y"}, candidates, 2)


def test_bigger():
    """20 навыков, 12 кандидатов"""
    needed = {f"s{i}" for i in range(20)}
    candidates = {f"c{k}": {f"s{i}" for i in range(20) if (i * 7 + k) % 5 == 0 or i % 12 == k} for k in range(12)}
    _check(needed, candidates, 7)

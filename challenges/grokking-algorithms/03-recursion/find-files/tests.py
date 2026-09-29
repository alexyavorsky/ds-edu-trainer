def test_example():
    """Пример из условия"""
    project = {
        "main.py": 120,
        "README.md": 40,
        "utils": {"io.py": 300, "data.csv": 900, "deep": {"cfg.py": 10}},
    }
    got = find_files(project, ".py")
    expected = ["main.py", "utils/io.py", "utils/deep/cfg.py"]
    assert got == expected, f"ожидалось {expected}, получено {got!r}"


def test_empty_folder():
    """Пустая папка → []"""
    got = find_files({}, ".py")
    assert got == [], f"ожидалось [], получено {got!r}"


def test_no_matches():
    """Нет подходящих файлов → [] (в том числе notes.py.bak — у него расширение .bak)"""
    got = find_files({"a.txt": 1, "b": {"c.md": 2, "notes.py.bak": 3}}, ".py")
    assert got == [], f"ожидалось [], получено {got!r}"


def test_only_top_level():
    """Файлы только на верхнем уровне — пути без префикса"""
    got = find_files({"a.py": 1, "b.txt": 2, "c.py": 3}, ".py")
    assert got == ["a.py", "c.py"], f"ожидалось ['a.py', 'c.py'], получено {got!r}"


def test_empty_subfolders():
    """Пустые подпапки не ломают обход"""
    got = find_files({"x": {}, "y": {"z": {}}, "k.py": 5}, ".py")
    assert got == ["k.py"], f"ожидалось ['k.py'], получено {got!r}"


def test_folder_named_like_file():
    """Папка «old.py» не попадает в ответ, но её содержимое ищется"""
    got = find_files({"old.py": {"new.py": 1}}, ".py")
    assert got == ["old.py/new.py"], f"ожидалось ['old.py/new.py'], получено {got!r}"


def test_same_names_in_different_folders():
    """Одинаковые имена в разных папках — оба пути"""
    got = find_files({"a": {"x.py": 1}, "b": {"x.py": 2}}, ".py")
    assert got == ["a/x.py", "b/x.py"], f"ожидалось ['a/x.py', 'b/x.py'], получено {got!r}"


def test_deep_nesting():
    """Глубина 50 уровней"""
    folder: dict = {"end.py": 1}
    for i in range(49, -1, -1):
        folder = {f"d{i}": folder}
    expected = "/".join(f"d{i}" for i in range(50)) + "/end.py"
    got = find_files(folder, ".py")
    assert got == [expected], f"ожидался один путь длиной {len(expected)}, получено {got!r:.80}"

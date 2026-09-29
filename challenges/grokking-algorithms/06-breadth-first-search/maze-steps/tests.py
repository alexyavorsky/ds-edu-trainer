def test_example():
    """Пример из условия → 4"""
    got = maze_steps(["S.#", ".##", "..E"])
    assert got == 4, f"ожидалось 4, получено {got!r}"


def test_adjacent():
    """Выход рядом → 1"""
    got = maze_steps(["SE"])
    assert got == 1, f"ожидалось 1, получено {got!r}"


def test_blocked():
    """Выход замурован → -1"""
    got = maze_steps(["S.#", "###", "#.E"])
    assert got == -1, f"ожидалось -1, получено {got!r}"


def test_one_column():
    """Узкий коридор в одну клетку шириной"""
    got = maze_steps(["S", ".", ".", "E"])
    assert got == 3, f"ожидалось 3, получено {got!r}"


def test_shortest_of_two():
    """Из двух путей выбирается короткий"""
    maze = [
        "S....",
        ".###.",
        ".#E..",
        ".###.",
        ".....",
    ]
    got = maze_steps(maze)
    assert got == 8, f"ожидалось 8 (верхний путь; нижний — 12), получено {got!r}"


def test_no_wrap_around():
    """С края поля нельзя «перепрыгнуть» на другой край"""
    got = maze_steps(["E#S"])
    assert got == -1, f"ожидалось -1, получено {got!r}"


def test_big_open_field():
    """Открытое поле 60×60 из угла в угол"""
    maze = ["." * 60 for _ in range(60)]
    maze[0] = "S" + maze[0][1:]
    maze[-1] = maze[-1][:-1] + "E"
    got = maze_steps(maze)
    assert got == 118, f"ожидалось 118, получено {got!r}"

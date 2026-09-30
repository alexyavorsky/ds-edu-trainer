# Урок np-project-pixels. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% show
import numpy as np


def show(picture):
    for row in picture:          # цикл for по таблице перебирает её строки
        line = ""
        for value in row:        # а по строке — её элементы
            if value:
                line += "█"      # 1 — закрашенная точка
            else:
                line += "·"      # 0 — пустая
        print(line)


show(np.zeros((3, 8), dtype=int))

# %% frame [exercise]
frame = np.zeros((6, 10), dtype=int)
frame[0] = 1
frame[-1] = 1
frame[:, 0] = 1
frame[:, -1] = 1
show(frame)
# ─── заготовка ───
frame = np.zeros((6, 10), dtype=int)
# ─── проверка ───
def test_frame():
    "по краям — единицы, внутри — нули"
    got = frame.tolist()
    assert got[0] == [1] * 10 and got[-1] == [1] * 10, "верхняя и нижняя строки должны быть закрашены: frame[0] = 1 и frame[-1] = 1"
    assert all(r[0] == 1 and r[-1] == 1 for r in got), "левый и правый столбцы должны быть закрашены: frame[:, 0] = 1 и frame[:, -1] = 1"
    assert all(v == 0 for r in got[1:-1] for v in r[1:-1]), "внутри рамки должны остаться нули"
# ─── другое решение ───
frame = np.ones((6, 10), dtype=int)
frame[1:-1, 1:-1] = 0
# ─── ошибка ───
frame = np.zeros((6, 10), dtype=int)
frame[0] = 1
frame[-1] = 1
frame[0, :] = 1
frame[-1, :] = 1

# %% plus [exercise]
plus = np.zeros((7, 7), dtype=int)
plus[3] = 1
plus[:, 3] = 1
# ─── заготовка ───
plus = np.zeros((7, 7), dtype=int)
# ─── проверка ───
def test_plus():
    "закрашены средняя строка и средний столбец"
    got = plus.tolist()
    assert got[3] == [1] * 7, "средняя строка (индекс 3) должна быть закрашена: plus[3] = 1"
    assert all(r[3] == 1 for r in got), "средний столбец (индекс 3) должен быть закрашен: plus[:, 3] = 1"
    assert sum(map(sum, got)) == 13, "закрашено лишнее: кроме средней строки и столбца всё должно остаться нулём"
# ─── другое решение ───
plus = np.zeros((7, 7), dtype=int)
plus[3, :] = 1
plus[:, 3] = 1
# ─── ошибка ───
plus = np.zeros((7, 7), dtype=int)
plus[3] = 1
plus[3] = 1

# %% count [exercise]
lit = plus.sum()
# ─── заготовка ───
lit = ...
# ─── проверка ───
def test_lit():
    "lit — число закрашенных точек"
    assert lit != 14, "14 — это 7 + 7, но центр креста закрашен и строкой, и столбцом: точка там одна"
    assert lit != 49, "49 — это все точки холста, а нужны только закрашенные: сумма единиц"
    assert lit == 13, f"lit = {lit}, а закрашено 13 точек"
# ─── другое решение ───
lit = np.sum(plus)
# ─── ошибка ───
lit = plus.size
# ─── ошибка ───
lit = len(plus) + len(plus)

# %% count-print
show(plus)
print("закрашено:", lit)

# %% arrow
up = np.array([
    [0, 0, 1, 0, 0],
    [0, 1, 1, 1, 0],
    [1, 0, 1, 0, 1],
    [0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0],
])
right = np.array([
    [0, 0, 1, 0, 0],
    [0, 0, 0, 1, 0],
    [1, 1, 1, 1, 1],
    [0, 0, 0, 1, 0],
    [0, 0, 1, 0, 0],
])
show(up)

# %% flip [exercise]
down = up[::-1]
show(down)
# ─── заготовка ───
down = ...
# ─── проверка ───
def test_down():
    "down — стрелка вниз"
    assert isinstance(down, np.ndarray) and down.shape == (5, 5), "down — это должна быть картинка 5 × 5"
    got = down.tolist()
    assert got != up.tolist(), "картинка не изменилась: строки нужно переставить в обратном порядке — up[::-1]"
    assert got == [[0, 0, 1, 0, 0], [0, 0, 1, 0, 0], [1, 0, 1, 0, 1], [0, 1, 1, 1, 0], [0, 0, 1, 0, 0]], "это не отражение сверху вниз: переставьте строки — up[::-1]"
# ─── другое решение ───
down = up[4::-1]
# ─── ошибка ───
down = up[:, ::-1]

# %% mirror [exercise]
left = right[:, ::-1]
show(left)
# ─── заготовка ───
left = ...
# ─── проверка ───
def test_left():
    "left — стрелка влево"
    assert isinstance(left, np.ndarray) and left.shape == (5, 5), "left — это должна быть картинка 5 × 5"
    got = left.tolist()
    assert got != right.tolist(), "картинка не изменилась: столбцы нужно переставить в обратном порядке — right[:, ::-1]"
    assert got == [[0, 0, 1, 0, 0], [0, 1, 0, 0, 0], [1, 1, 1, 1, 1], [0, 1, 0, 0, 0], [0, 0, 1, 0, 0]], "это не отражение слева направо: переставьте столбцы — right[:, ::-1]"
# ─── другое решение ───
left = right.T[::-1].T
# ─── ошибка ───
left = right[::-1]

# %% rotate [exercise]
letter = np.array([
    [1, 1, 1],
    [1, 0, 0],
    [1, 0, 0],
    [1, 0, 0],
])
turned = letter.T[:, ::-1]
show(turned)
# ─── заготовка ───
letter = np.array([
    [1, 1, 1],
    [1, 0, 0],
    [1, 0, 0],
    [1, 0, 0],
])
turned = ...
# ─── проверка ───
def test_turned():
    "turned — буква Г, повёрнутая по часовой стрелке"
    assert isinstance(turned, np.ndarray), f"turned — это {type(turned).__name__}, а нужна картинка — массив"
    assert turned.shape == (3, 4), f"форма turned — {turned.shape}, а после поворота картинка 4 × 3 становится 3 × 4"
    got = turned.tolist()
    assert got != [[1, 1, 1, 1], [1, 0, 0, 0], [1, 0, 0, 0]], "это только .T — отражение по диагонали, а не поворот: после .T отразите столбцы, [:, ::-1]"
    assert got != [[1, 0, 0, 0], [1, 0, 0, 0], [1, 1, 1, 1]], "это поворот против часовой стрелки. После .T отражайте столбцы, а не строки"
    assert got == [[1, 1, 1, 1], [0, 0, 0, 1], [0, 0, 0, 1]], "это не поворот буквы по часовой стрелке: сначала letter.T, потом [:, ::-1]"
# ─── другое решение ───
letter = np.array([
    [1, 1, 1],
    [1, 0, 0],
    [1, 0, 0],
    [1, 0, 0],
])
turned = letter[::-1].T
# ─── ошибка ───
letter = np.array([
    [1, 1, 1],
    [1, 0, 0],
    [1, 0, 0],
    [1, 0, 0],
])
turned = letter.T
# ─── ошибка ───
letter = np.array([
    [1, 1, 1],
    [1, 0, 0],
    [1, 0, 0],
    [1, 0, 0],
])
turned = letter.T[::-1]

# %% crop [exercise]
photo = np.arange(64).reshape(8, 8)
center = photo[2:6, 2:6]
# ─── заготовка ───
photo = np.arange(64).reshape(8, 8)
center = ...
# ─── проверка ───
def test_center():
    "center — квадрат 4 × 4 из середины"
    assert isinstance(center, np.ndarray), f"center — это {type(center).__name__}, а нужен блок массива photo"
    assert center.shape == (4, 4), f"форма center — {center.shape}, а нужно (4, 4): строки 2:6 и столбцы 2:6"
    assert center.tolist()[0] == [18, 19, 20, 21], "квадрат должен начинаться со строки 2 и столбца 2"
# ─── другое решение ───
photo = np.arange(64).reshape(8, 8)
center = photo[2:-2, 2:-2]
# ─── ошибка ───
photo = np.arange(64).reshape(8, 8)
center = photo[2:5, 2:5]

# %% final
for picture in (frame, down, left, turned):
    show(picture)
    print()

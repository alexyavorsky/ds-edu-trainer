# Урок np-solve. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% solve
import numpy as np

A_demo = np.array([[3, 2], [1, 4]])
b_demo = np.array([690, 730])
x = np.linalg.solve(A_demo, b_demo)
print(np.round(x, 2))                   # пачка кофе и кружка
print(np.round(A_demo @ x, 2))          # умножили обратно — получили суммы чеков
print(np.allclose(A_demo @ x, b_demo))

# %% two [exercise]
A = np.array([[2, 1], [1, 3]])
b = np.array([520, 560])
cafe_prices = np.linalg.solve(A, b)
# ─── заготовка ───
A = ...
b = ...
cafe_prices = ...
# ─── проверка ───
def test_system():
    "A и b — система из двух чеков"
    assert np.shape(A) == (2, 2), f"у A форма {np.shape(A)}, а нужна (2, 2): два чека × два товара"
    assert np.shape(b) == (2,), f"у b форма {np.shape(b)}, а чеков два: [520, 560]"


def test_prices():
    "cafe_prices — цены латте и круассана"
    assert np.shape(cafe_prices) == (2,), "cafe_prices — две цены: np.linalg.solve(A, b)"
    assert not np.allclose(cafe_prices, [120, 200]), "цены в обратном порядке: столбцы A — сначала латте, потом круассан"
    assert np.allclose(cafe_prices, [200, 120]), f"cafe_prices = {np.round(cafe_prices, 2)}, а латте стоит 200 ₽, круассан — 120 ₽: проверьте строки A"
# ─── другое решение ───
A = np.array([
    [2, 1],
    [1, 3],
])
b = np.array([520, 560])
cafe_prices = np.linalg.solve(A, b)
# ─── ошибка ───
A = np.array([[1, 2], [3, 1]])
b = np.array([520, 560])
cafe_prices = np.linalg.solve(A, b)
# ─── ошибка ───
A = np.array([[2, 1], [1, 3]])
b = np.array([560, 520])
cafe_prices = np.linalg.solve(A, b)

# %% receipts [exercise]
A3 = np.array([[2, 1, 1], [1, 3, 0], [0, 2, 2]])
b3 = np.array([690, 720, 900])
unit_prices = np.linalg.solve(A3, b3)
# ─── заготовка ───
A3 = ...
b3 = ...
unit_prices = ...
# ─── проверка ───
def test_system():
    "A3 и b3 — система из трёх чеков"
    assert np.shape(A3) == (3, 3), f"у A3 форма {np.shape(A3)}, а нужна (3, 3): три чека × три позиции"
    assert np.shape(b3) == (3,), f"у b3 форма {np.shape(b3)}, а чеков три"


def test_prices():
    "unit_prices — цены кофе, чая и пирожного"
    assert np.shape(unit_prices) == (3,), "unit_prices — три цены: np.linalg.solve(A3, b3)"
    assert np.allclose(unit_prices, [120, 200, 250]), f"unit_prices = {np.round(unit_prices, 2)}, а кофе 120 ₽, чай 200 ₽, пирожное 250 ₽ — проверьте строки A3: позиции нет в чеке — 0"
# ─── другое решение ───
A3 = np.array([
    [2, 1, 1],
    [1, 3, 0],
    [0, 2, 2],
])
b3 = np.array([690, 720, 900])
unit_prices = np.linalg.solve(A3, b3)
# ─── ошибка ───
A3 = np.array([[2, 1, 0], [1, 3, 2], [1, 0, 2]])
b3 = np.array([690, 720, 900])
unit_prices = np.linalg.solve(A3, b3)

# %% blend [exercise]
blend = np.linalg.solve(np.array([[1, 1], [800, 1200]]), np.array([10, 9500]))
# ─── заготовка ───
blend = ...
# ─── проверка ───
def test_blend():
    "blend — килограммы дешёвого и дорогого сорта"
    assert np.shape(blend) == (2,), "blend — два числа: сколько килограммов каждого сорта"
    assert abs(np.sum(blend) - 10) < 1e-9, f"в сумме {np.sum(blend):.2f} кг, а смеси нужно 10 кг: первое уравнение — x + y = 10"
    assert not np.allclose(blend, [3.75, 6.25]), "сорта в обратном порядке: сначала дешёвый (800 ₽/кг), потом дорогой"
    assert np.allclose(blend, [6.25, 3.75]), f"blend = {np.round(blend, 2)}, а нужно 6.25 кг дешёвого и 3.75 кг дорогого: стоимость всей смеси — 10 × 950 = 9500"
# ─── другое решение ───
weights_and_costs = np.array([[1, 1], [800, 1200]])
totals = np.array([10, 10 * 950])
blend = np.linalg.solve(weights_and_costs, totals)
# ─── ошибка ───
blend = np.linalg.solve(np.array([[1, 1], [800, 1200]]), np.array([10, 950]))
# ─── ошибка ───
blend = np.linalg.solve(np.array([[1, 1], [1200, 800]]), np.array([10, 9500]))

# %% singular [platform]
same = np.array([[3, 2], [6, 4]])      # второй чек — первый, умноженный на два
try:
    print(np.linalg.solve(same, np.array([690, 1380])))
except np.linalg.LinAlgError as error:
    print("LinAlgError:", error)

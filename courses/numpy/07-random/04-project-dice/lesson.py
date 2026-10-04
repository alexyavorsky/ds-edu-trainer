# Урок np-project-dice. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% fair [exercise]
import numpy as np

rng = np.random.default_rng(7)
rolls = rng.integers(1, 7, size=60000)
faces = np.bincount(rolls)[1:]
worst_gap = (faces - 10000).max()
# ─── заготовка ───
import numpy as np

faces = ...
worst_gap = ...
# ─── проверка ───
def test_faces():
    "faces — выпадения граней 1–6"
    assert isinstance(faces, np.ndarray), f"faces — это {type(faces).__name__}, а нужен массив из np.bincount"
    assert len(faces) == 6, f"в faces {len(faces)} чисел, а граней 6: уберите нулевую"
    assert faces.sum() == 60000, f"сумма faces — {faces.sum()}, а бросков 60 000"
    assert faces.tolist() == [9899, 9981, 9959, 9876, 10153, 10132], "броски не те: генератор с seed 7, 60 000 бросков"


def test_gap():
    "worst_gap — наибольшее отклонение вверх от 10 000"
    assert worst_gap != 10153, "10153 — само число выпадений, а нужно отклонение от 10 000"
    assert worst_gap == 153, f"worst_gap = {worst_gap} — это не наибольшее отклонение вверх от 10 000"
# ─── другое решение ───
import numpy as np

rolls = np.random.default_rng(7).integers(1, 7, 60000)
faces = np.bincount(rolls, minlength=7)[1:]
worst_gap = faces.max() - 10000
# ─── ошибка ───
import numpy as np

rolls = np.random.default_rng(7).integers(1, 7, 60000)
faces = np.bincount(rolls)[1:]
worst_gap = faces.max()

# %% three [exercise]
rng = np.random.default_rng(9)
sums3 = rng.integers(1, 7, size=(20000, 3)).sum(axis=1)
common_sum = np.bincount(sums3).argmax()
# ─── заготовка ───
sums3 = ...
common_sum = ...
# ─── проверка ───
def test_sums():
    "sums3 — 20 000 сумм трёх кубиков"
    assert isinstance(sums3, np.ndarray) and sums3.shape == (20000,), "sums3 — 20 000 сумм: таблица 20000 × 3, сумма по строкам"
    assert sums3.min() >= 3 and sums3.max() <= 18, f"суммы от {sums3.min()} до {sums3.max()}, а у трёх кубиков — от 3 до 18"
    assert abs(sums3.mean() - 10.5) < 0.1, "средняя сумма должна быть около 10.5: складывайте по строкам"


def test_common():
    "common_sum — самая частая сумма"
    assert common_sum != 2550, "2550 — сколько раз выпала самая частая сумма; сама сумма — это индекс в результате bincount"
    assert common_sum == 10, f"common_sum = {common_sum}: проверьте seed 9 и таблицу 20000 × 3"
# ─── другое решение ───
throws = np.random.default_rng(9).integers(1, 7, size=(20000, 3))
sums3 = throws[:, 0] + throws[:, 1] + throws[:, 2]
values, counts = np.unique(sums3, return_counts=True)
common_sum = values[counts.argmax()]
# ─── ошибка ───
sums3 = np.random.default_rng(9).integers(1, 7, size=(20000, 3)).sum(axis=1)
common_sum = np.bincount(sums3).max()

# %% cube
face = np.arange(1, 7)
first = face[:, np.newaxis, np.newaxis]     # (6, 1, 1): грани первого кубика — по оси 0
second = face[np.newaxis, :, np.newaxis]    # (1, 6, 1): второго — по оси 1
third = face                                # (6,) — это как (1, 1, 6): третьего — по оси 2
print(first.shape, second.shape, third.shape)
all_sums = first + second + third
print(all_sums.shape, all_sums.size)
print(all_sums[0])          # таблица 6 × 6: на первом кубике 1, строки — второй кубик, столбцы — третий
print(all_sums[2, 3, 4])    # 3 + 4 + 5
print(np.bincount(all_sums.ravel())[3:])    # сколько исходов дают сумму 3, 4, …, 18

# %% exact [exercise]
p10 = (all_sums == 10).mean()
sim_p10 = (sums3 == 10).mean()
# ─── заготовка ───
p10 = ...
sim_p10 = ...
# ─── проверка ───
def test_exact():
    "p10 — точная вероятность суммы 10"
    assert p10 != 27, "27 — число исходов с суммой 10; вероятность — их доля: среднее маски"
    assert abs(p10 - 27 / 216) < 1e-12, f"p10 = {p10} — это не точная вероятность суммы 10"


def test_sim():
    "sim_p10 — та же вероятность по моделированию"
    assert abs(sim_p10 - 0.1275) < 1e-9, f"sim_p10 = {sim_p10} — это не доля сумм 10 среди бросков sums3"
# ─── другое решение ───
p10 = (all_sums == 10).sum() / all_sums.size
sim_p10 = np.mean(sums3 == 10)
# ─── ошибка ───
p10 = (all_sums == 10).sum()
sim_p10 = (sums3 == 10).mean()

# %% game [exercise]
win_p = (all_sums >= 15).mean()
expected = win_p * 100 - 10
sim_expected = (sums3 >= 15).mean() * 100 - 10
# ─── заготовка ───
win_p = ...
expected = ...
sim_expected = ...
# ─── проверка ───
def test_win():
    "win_p — точная вероятность 15 и больше"
    assert abs(win_p - 15 / 216) > 1e-12, "это вероятность суммы больше 15; условие — 15 и больше: >="
    assert abs(win_p - 20 / 216) < 1e-12, f"win_p = {win_p} — это не точная вероятность суммы 15 и больше"


def test_expected():
    "expected и sim_expected — средний результат игры"
    assert abs(expected - (20 / 216 * 100 - 10)) < 1e-9, f"expected = {expected} — это не средний результат игры по точной вероятности"
    assert abs(sim_expected - (-0.67)) < 1e-9, f"sim_expected = {sim_expected} — это не средний результат игры по моделированию"
# ─── другое решение ───
win_p = np.mean(all_sums >= 15)
expected = 100 * win_p - 10
sim_expected = 100 * np.mean(sums3 >= 15) - 10
# ─── ошибка ───
win_p = (all_sums > 15).mean()
expected = win_p * 100 - 10
sim_expected = (sums3 > 15).mean() * 100 - 10
# ─── ошибка ───
win_p = (all_sums >= 15).mean()
expected = win_p * 100
sim_expected = (sums3 >= 15).mean() * 100

# %% summary
print("выигрышных исходов:", (all_sums >= 15).sum(), "из", all_sums.size)
print("точно:", round(win_p, 4), "→ средний результат", round(expected, 2), "₽")
print("моделирование:", round((sums3 >= 15).mean(), 4), "→", round(sim_expected, 2), "₽")

# Урок np-distances. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% norm
import numpy as np

v = np.array([3, 4])
print(np.sqrt((v ** 2).sum()))
print(np.linalg.norm(v))

a = np.array([1, 1])
b = np.array([4, 5])
print(np.linalg.norm(a - b))     # расстояние между точками a и b

# %% norm-quiz [quiz]
print(np.linalg.norm(np.array([6, 8])))

# %% to-many
cafes = np.array([[0, 0], [2, 1], [5, 5]])
me = np.array([1, 1])
print(cafes - me)                            # разность с каждой строкой
print(np.linalg.norm(cafes - me, axis=1))    # длина каждой строки — три расстояния

# %% nearest [exercise]
shops = np.array([
    [1.0, 2.0],
    [4.0, 6.0],
    [-2.0, 3.0],
    [3.0, -1.0],
    [0.5, 5.0],
    [6.0, 2.0],
])
home = np.array([2.0, 3.0])
dists = np.linalg.norm(shops - home, axis=1)
nearest = dists.argmin()
# ─── заготовка ───
shops = np.array([
    [1.0, 2.0],
    [4.0, 6.0],
    [-2.0, 3.0],
    [3.0, -1.0],
    [0.5, 5.0],
    [6.0, 2.0],
])
home = np.array([2.0, 3.0])
dists = ...
nearest = ...
# ─── проверка ───
def test_dists():
    "dists — расстояния до шести магазинов"
    assert isinstance(dists, np.ndarray), "dists — одно число: без axis=1 norm считает длину всей таблицы"
    assert dists.shape == (6,), f"у dists форма {dists.shape}, а магазинов 6: норма каждой строки — axis=1"
    assert np.allclose(dists, [1.414214, 3.605551, 4.0, 4.123106, 2.5, 4.123106], atol=1e-5), f"dists = {np.round(dists, 3)}, а должно быть ≈ [1.414, 3.606, 4, 4.123, 2.5, 4.123]"


def test_nearest():
    "nearest — номер ближайшего магазина"
    assert nearest == 0, f"nearest = {nearest}, а ближе всех магазин в строке 0 (≈ 1.41 км)"
# ─── другое решение ───
shops = np.array([
    [1.0, 2.0],
    [4.0, 6.0],
    [-2.0, 3.0],
    [3.0, -1.0],
    [0.5, 5.0],
    [6.0, 2.0],
])
home = np.array([2.0, 3.0])
dists = np.sqrt(((shops - home) ** 2).sum(axis=1))
nearest = np.argmin(dists)
# ─── ошибка ───
shops = np.array([
    [1.0, 2.0],
    [4.0, 6.0],
    [-2.0, 3.0],
    [3.0, -1.0],
    [0.5, 5.0],
    [6.0, 2.0],
])
home = np.array([2.0, 3.0])
dists = np.linalg.norm(shops - home)
nearest = 0

# %% pairwise
pts = np.array([[0, 0], [3, 4], [6, 0]])
diff = pts[:, np.newaxis, :] - pts[np.newaxis, :, :]
print(diff.shape)
print(diff[1, 0])          # pts[1] - pts[0]
table = np.linalg.norm(diff, axis=2)
print(table)

# %% farthest [exercise]
towns = np.array([[0, 0], [3, 4], [6, 0], [7, 5], [2, 9]])
dist = np.linalg.norm(towns[:, np.newaxis, :] - towns[np.newaxis, :, :], axis=2)
max_dist = dist.max()
# ─── заготовка ───
towns = np.array([[0, 0], [3, 4], [6, 0], [7, 5], [2, 9]])
dist = ...
max_dist = ...
# ─── проверка ───
def test_dist():
    "dist — таблица 5 × 5"
    assert isinstance(dist, np.ndarray), f"dist — это {type(dist).__name__}, а нужна таблица расстояний"
    assert dist.shape != (5, 5, 2), "у dist форма (5, 5, 2) — это разности; норма по последней оси: axis=2"
    assert dist.shape == (5, 5), f"у dist форма {dist.shape}, а нужна (5, 5): все пары пяти городов"
    assert abs(dist[0, 1] - 5) < 1e-9, "от города 0 до города 1 должно быть 5: проверьте разности"


def test_max():
    "max_dist — наибольшее расстояние"
    assert np.shape(max_dist) == (), "max_dist — массив, а нужно одно число: max без axis"
    assert abs(max_dist - 9.848858) < 1e-5, f"max_dist = {max_dist}, а дальше всего друг от друга города 2 и 4 — ≈ 9.85"
# ─── другое решение ───
towns = np.array([[0, 0], [3, 4], [6, 0], [7, 5], [2, 9]])
diff_all = towns[:, np.newaxis] - towns
dist = np.sqrt((diff_all ** 2).sum(axis=2))
max_dist = np.max(dist)
# ─── ошибка ───
towns = np.array([[0, 0], [3, 4], [6, 0], [7, 5], [2, 9]])
dist = np.linalg.norm(towns[:, np.newaxis, :] - towns[np.newaxis, :, :], axis=2)
max_dist = dist.max(axis=0)

# %% neighbor
demo = table.copy()
np.fill_diagonal(demo, np.inf)
print(demo)
print(demo.argmin(axis=1))

# %% closest [exercise]
no_self = dist.copy()
np.fill_diagonal(no_self, np.inf)
neighbor = no_self.argmin(axis=1)
neighbor_dist = no_self.min(axis=1)
# ─── заготовка ───
no_self = ...
neighbor = ...
neighbor_dist = ...
# ─── проверка ───
def test_dist_kept():
    "dist не изменился"
    assert (dist.diagonal() == 0).all(), "в dist изменилась диагональ: заполняйте копию — dist.copy()"


def test_neighbor():
    "neighbor — ближайший другой город"
    assert np.shape(neighbor) == (5,), f"у neighbor форма {np.shape(neighbor)}, а городов 5: argmin по строкам, axis=1"
    assert neighbor.tolist() != [0, 1, 2, 3, 4], "каждый город ближе всего к самому себе: заполните диагональ np.inf"
    assert neighbor.tolist() == [1, 3, 1, 1, 1], f"neighbor = {neighbor.tolist()}, а ближайшие соседи — [1, 3, 1, 1, 1]"


def test_neighbor_dist():
    "neighbor_dist — расстояние до ближайшего"
    assert np.shape(neighbor_dist) == (5,), "neighbor_dist — пять расстояний: min по axis=1"
    assert np.allclose(neighbor_dist, [5.0, 4.123106, 5.0, 4.123106, 5.09902], atol=1e-5), f"neighbor_dist = {np.round(neighbor_dist, 3)}"
# ─── другое решение ───
no_self = dist + 0
np.fill_diagonal(no_self, np.inf)
neighbor = np.argmin(no_self, axis=1)
neighbor_dist = np.min(no_self, axis=1)
# ─── ошибка ───
no_self = dist.copy()
neighbor = no_self.argmin(axis=1)
neighbor_dist = no_self.min(axis=1)
# ─── ошибка ───
no_self = dist
np.fill_diagonal(no_self, np.inf)
neighbor = no_self.argmin(axis=1)
neighbor_dist = no_self.min(axis=1)

# Урок np-project-knn. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% data
import numpy as np

drinks = np.array(["эспрессо", "капучино", "латте", "раф", "чай", "какао"])
ratings = np.array([
    [5, 4, 2, 1, 2, 1],
    [2, 3, 5, 5, 3, 5],
    [4, 5, 3, 2, 1, 2],
    [1, 2, 4, 5, 4, 4],
    [5, 5, 3, 2, 2, 1],
    [3, 3, 3, 3, 5, 3],
    [2, 2, 5, 4, 3, 5],
    [4, 3, 2, 2, 4, 2],
])
olya = np.array([2, 3, 5, 4, 3])     # без какао
print(ratings.shape, olya.shape)
print(drinks[:5])

# %% similar [exercise]
dists = np.linalg.norm(ratings[:, :5] - olya, axis=1)
# ─── заготовка ───
dists = ...
# ─── проверка ───
def test_dists():
    "dists — расстояния до восьми гостей"
    assert isinstance(dists, np.ndarray), "dists — одно число: norm без axis=1 считает всю таблицу разом"
    assert dists.shape == (8,), f"у dists форма {dists.shape}, а гостей 8"
    assert np.allclose(dists, [5.385165, 1.0, 4.472136, 2.236068, 4.690416, 3.162278, 1.0, 4.242641], atol=1e-5), (
        f"dists = {np.round(dists, 3)}: сравнивайте только первые пять столбцов — ratings[:, :5]"
    )
# ─── другое решение ───
diff = ratings[:, :5] - olya
dists = np.sqrt((diff ** 2).sum(axis=1))
# ─── ошибка ───
dists = np.linalg.norm(ratings[:, :5] - olya)

# %% neighbors [exercise]
neighbors = np.argsort(dists)[:3]
# ─── заготовка ───
neighbors = ...
# ─── проверка ───
def test_neighbors():
    "neighbors — три ближайших гостя"
    assert isinstance(neighbors, np.ndarray), f"neighbors — это {type(neighbors).__name__}, а нужен массив номеров"
    assert len(neighbors) == 3, f"в neighbors {len(neighbors)} номеров, а соседей нужно три: [:3]"
    assert sorted(neighbors.tolist()) != [0, 2, 4], "это три самых далёких гостя: argsort упорядочивает по возрастанию, ближние — в начале"
    assert sorted(neighbors.tolist()) == [1, 3, 6], f"neighbors = {neighbors.tolist()}, а ближе всех к Оле гости 1, 6 и 3"
# ─── другое решение ───
order = np.argsort(dists)
neighbors = order[0:3]
# ─── ошибка ───
neighbors = np.argsort(dists)[-3:]

# %% predict [exercise]
cocoa_pred = ratings[neighbors][:, 5].mean()
# ─── заготовка ───
cocoa_pred = ...
# ─── проверка ───
def test_pred():
    "cocoa_pred — прогноз оценки какао"
    assert np.shape(cocoa_pred) == (), "cocoa_pred — массив, а нужно одно число: средняя столбца 5 у соседей"
    assert abs(cocoa_pred - 2.875) > 1e-6, "это средняя какао у всех гостей; нужна — у трёх соседей: ratings[neighbors]"
    assert abs(cocoa_pred - 14 / 3) < 1e-9, f"cocoa_pred = {cocoa_pred}, а у соседей какао в среднем ≈ 4.67"
# ─── другое решение ───
cocoa_pred = np.mean(ratings[neighbors, 5])
# ─── ошибка ───
cocoa_pred = ratings[:, 5].mean()

# %% recommend
print(np.round(ratings[neighbors].mean(axis=0), 1))
print(np.round(ratings.mean(axis=0), 1))

# %% days
days = np.array([
    # температура, выходной, акция
    [5, 0, 0],
    [12, 0, 1],
    [18, 1, 0],
    [22, 1, 1],
    [8, 1, 0],
    [25, 0, 0],
    [15, 0, 1],
    [19, 0, 0],
    [3, 1, 1],
    [16, 1, 0],
    [28, 1, 0],
    [10, 0, 0],
])
cups = np.array([140, 190, 260, 330, 250, 150, 200, 155, 280, 265, 240, 145])
tomorrow = np.array([17, 0, 0])
print(days.shape, cups.shape)

# %% naive [exercise]
naive_dists = np.linalg.norm(days - tomorrow, axis=1)
naive_nb = np.argsort(naive_dists)[:4]
naive_pred = cups[naive_nb].mean()
# ─── заготовка ───
naive_dists = ...
naive_nb = ...
naive_pred = ...
# ─── проверка ───
def test_dists():
    "naive_dists — расстояния до двенадцати дней"
    assert isinstance(naive_dists, np.ndarray) and naive_dists.shape == (12,), "naive_dists — 12 расстояний: norm по axis=1"


def test_nb():
    "naive_nb — четыре ближайших дня"
    assert len(naive_nb) == 4, f"в naive_nb {len(naive_nb)} номеров, а нужно четыре"
    assert sorted(naive_nb.tolist()) == [2, 6, 7, 9], f"naive_nb = {naive_nb.tolist()}, а по сырым признакам ближе всех дни 2, 9, 7 и 6"


def test_pred():
    "naive_pred — прогноз по сырым признакам"
    assert np.shape(naive_pred) == (), "naive_pred — одно число: средняя cups у соседей"
    assert naive_pred == 220, f"naive_pred = {naive_pred}, а средняя по четырём дням — 220"
# ─── другое решение ───
naive_dists = np.sqrt(((days - tomorrow) ** 2).sum(axis=1))
naive_nb = np.argsort(naive_dists)[0:4]
naive_pred = np.mean(cups[naive_nb])
# ─── ошибка ───
naive_dists = np.linalg.norm(days - tomorrow, axis=1)
naive_nb = np.argsort(naive_dists)[:4]
naive_pred = cups[:4].mean()

# %% naive-days
print(days[naive_nb])
print(cups[naive_nb])

# %% scaled [exercise]
lo = days.min(axis=0)
hi = days.max(axis=0)
days_n = (days - lo) / (hi - lo)
tomorrow_n = (tomorrow - lo) / (hi - lo)
scaled_nb = np.argsort(np.linalg.norm(days_n - tomorrow_n, axis=1))[:4]
scaled_pred = cups[scaled_nb].mean()
# ─── заготовка ───
lo = ...
hi = ...
days_n = ...
tomorrow_n = ...
scaled_nb = ...
scaled_pred = ...
# ─── проверка ───
def test_scale():
    "days_n и tomorrow_n — признаки на шкале 0–1"
    assert np.shape(lo) == (3,) and np.shape(hi) == (3,), "lo и hi — по числу на признак: min и max по axis=0"
    assert isinstance(days_n, np.ndarray) and days_n.shape == (12, 3), "days_n — таблица той же формы, что days"
    assert days_n.min() == 0 and days_n.max() == 1, "days_n должна быть от 0 до 1 в каждом столбце: (days - lo) / (hi - lo)"
    assert np.shape(tomorrow_n) == (3,), "tomorrow_n — три нормализованных признака завтрашнего дня"
    assert not np.isnan(tomorrow_n).any(), "в tomorrow_n есть nan: завтрашний день приводят теми же lo и hi, что и прошлые дни"
    assert np.allclose(tomorrow_n, [0.56, 0, 0]), f"tomorrow_n = {tomorrow_n}, а должно быть [0.56, 0, 0]: те же lo и hi, что для days"


def test_nb():
    "scaled_nb — четыре ближайших дня после нормализации"
    assert len(scaled_nb) == 4, f"в scaled_nb {len(scaled_nb)} номеров, а нужно четыре"
    assert sorted(scaled_nb.tolist()) == [0, 5, 7, 11], f"scaled_nb = {scaled_nb.tolist()}, а после нормализации ближе всех дни 7, 11, 5 и 0"


def test_pred():
    "scaled_pred — прогноз после нормализации"
    assert np.shape(scaled_pred) == (), "scaled_pred — одно число"
    assert scaled_pred == 147.5, f"scaled_pred = {scaled_pred}, а средняя по четырём дням — 147.5"
# ─── другое решение ───
lo = np.min(days, axis=0)
hi = np.max(days, axis=0)
span = hi - lo
days_n = (days - lo) / span
tomorrow_n = (tomorrow - lo) / span
scaled_dists = np.linalg.norm(days_n - tomorrow_n, axis=1)
scaled_nb = np.argsort(scaled_dists)[:4]
scaled_pred = cups[scaled_nb].mean()
# ─── ошибка ───
lo = days.min(axis=0)
hi = days.max(axis=0)
days_n = (days - lo) / (hi - lo)
tomorrow_n = (tomorrow - tomorrow.min()) / (tomorrow.max() - tomorrow.min())
scaled_nb = np.argsort(np.linalg.norm(days_n - tomorrow_n, axis=1))[:4]
scaled_pred = cups[scaled_nb].mean()

# %% summary
print("соседи без нормализации:", days[naive_nb][:, 1].sum(), "выходных из 4 →", naive_pred, "чашек")
print("соседи после нормализации:", days[scaled_nb][:, 1].sum(), "выходных из 4 →", scaled_pred, "чашек")

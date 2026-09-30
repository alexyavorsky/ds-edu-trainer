# Урок np-distributions. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% normal
import numpy as np

rng = np.random.default_rng(1)
heights = rng.normal(loc=170, scale=8, size=1000)
print(np.round(heights[:6], 1))
print(round(heights.mean(), 1), round(heights.std(), 1))

# %% within
print(((heights > 162) & (heights < 178)).mean())

# %% scores-sim [exercise]
rng = np.random.default_rng(10)
exam = rng.normal(loc=65, scale=12, size=500)
high_share = (exam > 80).mean()
# ─── заготовка ───
rng = ...
exam = ...
high_share = ...
# ─── проверка ───
def test_exam():
    "exam — 500 баллов со средним около 65 и отклонением около 12"
    assert isinstance(exam, np.ndarray) and exam.shape == (500,), "exam — 500 значений: rng.normal(..., size=500)"
    assert abs(exam.mean() - 65) < 2, f"среднее exam — {exam.mean():.1f}, а должно быть около 65: loc=65"
    assert abs(exam.std() - 12) < 2, f"отклонение exam — {exam.std():.1f}, а должно быть около 12: scale=12"


def test_share():
    "high_share — доля набравших больше 80"
    assert 0 < high_share < 1, f"high_share = {high_share} — доля должна быть между 0 и 1: среднее маски exam > 80"
    assert abs(exam[0] - 51.759939) < 1e-5, "exam получен не тем генератором: создайте его с seed 10 прямо перед normal"
    assert abs(high_share - 0.084) < 1e-9, f"high_share = {high_share}, а больше 80 набрали 8.4 % участников: среднее маски exam > 80"
# ─── другое решение ───
rng = np.random.default_rng(10)
exam = rng.normal(65, 12, 500)
high_share = np.mean(exam > 80)
# ─── ошибка ───
rng = np.random.default_rng(10)
exam = rng.normal(loc=12, scale=65, size=500)
high_share = (exam > 80).mean()

# %% uniform
rng = np.random.default_rng(2)
waits_demo = rng.uniform(0, 10, size=5)
print(np.round(waits_demo, 2))

# %% bus [exercise]
rng = np.random.default_rng(8)
waits = rng.uniform(0, 10, size=500)
long_share = (waits > 7).mean()
# ─── заготовка ───
rng = ...
waits = ...
long_share = ...
# ─── проверка ───
def test_waits():
    "waits — 500 ожиданий от 0 до 10 минут"
    assert isinstance(waits, np.ndarray) and waits.shape == (500,), "waits — 500 значений: rng.uniform(0, 10, size=500)"
    assert waits.min() >= 0 and waits.max() <= 10, f"значения от {waits.min():.2f} до {waits.max():.2f}, а должны быть от 0 до 10"


def test_share():
    "long_share — доля ожиданий дольше 7 минут"
    assert abs(waits.mean() - 4.948001) < 1e-5, "waits получены не тем генератором: seed 8, прямо перед uniform"
    assert abs(long_share - 0.292) < 1e-9, f"long_share = {long_share}, а дольше 7 минут ждали в 29.2 % случаев: среднее маски waits > 7"
# ─── другое решение ───
rng = np.random.default_rng(8)
waits = 10 * rng.random(500)
long_share = (waits > 7).sum() / 500
# ─── ошибка ───
rng = np.random.default_rng(8)
waits = rng.uniform(0, 10, size=500)
long_share = (waits < 7).mean()

# %% histogram
counts_demo, edges_demo = np.histogram(heights, bins=[140, 150, 160, 170, 180, 190, 200, 210])
print(counts_demo)
print(edges_demo)
print(counts_demo.sum())

# %% exam-hist [exercise]
counts, edges = np.histogram(exam, bins=[0, 40, 60, 80, 100])
# ─── заготовка ───
counts = ...
# ─── проверка ───
def test_counts():
    "counts — участники в четырёх интервалах"
    assert not isinstance(counts, tuple), "np.histogram вернула два массива: counts, edges = np.histogram(...)"
    assert isinstance(counts, np.ndarray), f"counts — это {type(counts).__name__}, а нужен массив количеств"
    assert len(counts) == 4, f"в counts {len(counts)} чисел, а интервалов 4 — границ должно быть 5: [0, 40, 60, 80, 100]"
    assert counts.tolist() == [11, 171, 276, 42], f"counts = {counts.tolist()}, а по интервалам 0–40, 40–60, 60–80, 80–100 должно быть [11, 171, 276, 42]"
# ─── другое решение ───
result = np.histogram(exam, bins=[0, 40, 60, 80, 100])
counts = result[0]
# ─── ошибка ───
counts = np.histogram(exam, bins=[0, 40, 60, 80, 100])
# ─── ошибка ───
counts, edges = np.histogram(exam, bins=4)

# %% hist-len [quiz]
print(len(np.histogram(np.arange(100), bins=[0, 25, 50, 75, 100])[0]))

# %% bincount
rolls_demo = np.random.default_rng(42).integers(1, 7, size=600)
print(np.bincount(rolls_demo))
print(np.bincount(rolls_demo)[1:])

# %% faces [exercise]
rolls = np.random.default_rng(4).integers(1, 7, size=1200)
faces = np.bincount(rolls)[1:]
top_face = faces.argmax() + 1
# ─── заготовка ───
rolls = ...
faces = ...
top_face = ...
# ─── проверка ───
def test_faces():
    "faces — выпадения граней 1–6"
    assert isinstance(faces, np.ndarray), f"faces — это {type(faces).__name__}, а нужен массив из np.bincount"
    assert len(faces) != 7, "в faces 7 чисел: уберите нулевую грань — np.bincount(rolls)[1:]"
    assert len(faces) == 6, f"в faces {len(faces)} чисел, а граней 6"
    assert faces.sum() == 1200, f"сумма faces — {faces.sum()}, а бросков 1200"


def test_top():
    "top_face — самая частая грань"
    assert faces.tolist() == [197, 197, 187, 190, 210, 219], "броски получены не тем генератором: seed 4, 1200 бросков"
    assert top_face != 5, "5 — индекс в faces; грань на единицу больше"
    assert top_face == 6, f"top_face = {top_face}, а чаще всех выпадала шестёрка"
# ─── другое решение ───
rng = np.random.default_rng(4)
rolls = rng.integers(1, 7, 1200)
faces = np.bincount(rolls, minlength=7)[1:]
top_face = np.argmax(faces) + 1
# ─── ошибка ───
rolls = np.random.default_rng(4).integers(1, 7, size=1200)
faces = np.bincount(rolls)
top_face = faces.argmax()
# ─── ошибка ───
rolls = np.random.default_rng(4).integers(1, 7, size=1200)
faces = np.bincount(rolls)[1:]
top_face = faces.argmax()

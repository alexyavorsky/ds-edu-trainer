# Урок np-random. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% rng
import numpy as np

rng = np.random.default_rng(0)
print(rng.integers(1, 11, size=5))
print(rng.random(3))
print(rng.integers(0, 100, size=(2, 4)))

# %% seed
a = np.random.default_rng(2025).integers(1, 100, size=5)
b = np.random.default_rng(2025).integers(1, 100, size=5)
print(a)
print(b)
print((a == b).all())

# %% dice [exercise]
rng = np.random.default_rng(42)
rolls = rng.integers(1, 7, size=20)
# ─── заготовка ───
rng = ...
rolls = ...
# ─── проверка ───
def test_rolls():
    "rolls — 20 бросков от 1 до 6"
    assert isinstance(rolls, np.ndarray), f"rolls — это {type(rolls).__name__}, а нужен массив: rng.integers(...)"
    assert len(rolls) == 20, f"бросков {len(rolls)}, а нужно 20: size=20"
    assert rolls.min() >= 1 and rolls.max() <= 6, f"значения от {rolls.min()} до {rolls.max()}, а у кубика — от 1 до 6: rng.integers(1, 7, ...)"


def test_seed():
    "генератор создан с seed 42"
    assert rolls.tolist() == [1, 5, 4, 3, 3, 6, 1, 5, 2, 1, 4, 6, 5, 5, 5, 5, 4, 1, 6, 3], (
        "числа не те: создайте генератор с seed 42 заново и сразу возьмите 20 бросков — np.random.default_rng(42)"
    )
# ─── другое решение ───
generator = np.random.default_rng(42)
rolls = generator.integers(1, 7, 20)
rng = generator
# ─── ошибка ───
rng = np.random.default_rng(42)
rolls = rng.integers(1, 6, size=20)
# ─── ошибка ───
rng = np.random.default_rng(42)
rolls = rng.integers(0, 7, size=20)

# %% events
rng = np.random.default_rng(1)
for n in [10, 100, 10000]:
    print(n, (rng.random(n) < 0.3).mean())

# %% coin [exercise]
rng = np.random.default_rng(3)
heads = rng.random(1000) < 0.5
share = heads.mean()
# ─── заготовка ───
rng = ...
heads = ...
share = ...
# ─── проверка ───
def test_heads():
    "heads — маска из 1000 бросков"
    assert isinstance(heads, np.ndarray), f"heads — это {type(heads).__name__}, а нужна маска: rng.random(1000) < 0.5"
    assert heads.dtype == bool, f"тип heads — {heads.dtype}, а маска — логический массив: сравните с 0.5"
    assert heads.shape == (1000,), f"у heads форма {heads.shape}, а бросков 1000"


def test_share():
    "share — доля орлов"
    assert abs(share - 0.502) < 1e-9, f"share = {share}, а с seed 3 доля орлов — 0.502: создайте генератор с seed 3 заново"
# ─── другое решение ───
rng = np.random.default_rng(3)
heads = rng.random(size=1000) < 0.5
share = heads.sum() / 1000
# ─── ошибка ───
rng = np.random.default_rng(3)
heads = rng.random(1000)
share = heads.mean()

# %% choice
rng = np.random.default_rng(11)
print(rng.choice(["орёл", "решка"], size=6))
print(rng.choice(np.arange(1, 11), size=5, replace=False))

# %% lottery [exercise]
rng = np.random.default_rng(7)
ticket = np.sort(rng.choice(np.arange(1, 50), size=6, replace=False))
# ─── заготовка ───
rng = ...
ticket = ...
# ─── проверка ───
def test_ticket():
    "ticket — шесть разных чисел от 1 до 49 по возрастанию"
    assert isinstance(ticket, np.ndarray) and len(ticket) == 6, "ticket — массив из 6 чисел: rng.choice(..., size=6, replace=False)"
    got = ticket.tolist()
    assert len(set(got)) == 6, f"в билете повторы {got}: добавьте replace=False"
    assert got == sorted(got), f"числа не по возрастанию {got}: np.sort(...)"
    assert min(got) >= 1 and max(got) <= 49, "числа должны быть от 1 до 49: np.arange(1, 50)"
    assert got == [28, 29, 32, 39, 42, 43], f"ticket = {got}: создайте генератор с seed 7 и выберите из np.arange(1, 50)"
# ─── другое решение ───
rng = np.random.default_rng(7)
balls = np.arange(1, 50)
ticket = np.sort(rng.choice(balls, 6, replace=False))
# ─── ошибка ───
rng = np.random.default_rng(7)
ticket = rng.choice(np.arange(1, 50), size=6, replace=False)

# %% winner [exercise]
speakers = ["Анна", "Иван", "Мария", "Олег"]
rng = np.random.default_rng(5)
first = rng.choice(speakers)
# ─── заготовка ───
speakers = ["Анна", "Иван", "Мария", "Олег"]
rng = ...
first = ...
# ─── проверка ───
def test_first():
    "first — одно имя из speakers"
    assert not isinstance(first, np.ndarray) or first.ndim == 0, "first — массив; без size метод choice вернёт одно имя"
    assert first in ["Анна", "Иван", "Мария", "Олег"], f"first = {first} — это не имя из списка speakers"
    assert first == "Мария", f"first = {first}: с seed 5 первой выпадает Мария — создайте генератор с seed 5"
# ─── другое решение ───
speakers = ["Анна", "Иван", "Мария", "Олег"]
rng = np.random.default_rng(5)
first = np.random.default_rng(5).choice(speakers)
# ─── ошибка ───
speakers = ["Анна", "Иван", "Мария", "Олег"]
rng = np.random.default_rng(5)
first = rng.choice(speakers, size=1)

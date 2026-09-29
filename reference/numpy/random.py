# Примеры к статье numpy/random.

# %% setup
rng = np.random.default_rng(42)   # генератор с фиксированным seed

# %% integers
print(rng.integers(1, 7, size=10))     # кубик: 1–6, верхняя граница не входит
rng.integers(0, 100, size=(2, 3))
# ─── вывод ───
# [1 5 4 3 3 6 1 5 2 1]
# array([[52, 97, 73],
#        [76, 71, 78]])

# %% floats
print(rng.random(3))                   # равномерно на [0, 1)
print(rng.uniform(10, 20, size=3))     # равномерно на [10, 20)
rng.normal(loc=170, scale=8, size=4).round(1)   # рост: среднее 170, отклонение 8
# ─── вывод ───
# [0.77395605 0.43887844 0.85859792]
# [16.97368029 10.94177348 19.75622352]
# array([171. , 167.5, 169.9, 163.2])

# %% choice
colors = np.array(["красный", "синий", "зелёный"])
print(rng.choice(colors, size=5))                          # с повторами
print(rng.choice(10, size=3, replace=False))               # без повторов
rng.choice(colors, size=5, p=[0.7, 0.2, 0.1])              # с вероятностями
# ─── вывод ───
# ['красный' 'зелёный' 'синий' 'синий' 'синий']
# [0 9 6]
# array(['зелёный', 'синий', 'синий', 'красный', 'красный'], dtype='<U7')

# %% shuffle
cards = np.arange(6)
print(rng.permutation(cards))   # новый перемешанный массив
rng.shuffle(cards)              # перемешать на месте
cards
# ─── вывод ───
# [3 2 5 4 1 0]
# array([2, 4, 0, 1, 3, 5])

# %% reproducible
a = np.random.default_rng(7).integers(0, 100, size=4)
b = np.random.default_rng(7).integers(0, 100, size=4)
a, b                            # тот же seed — те же числа
# ─── вывод ───
# (array([94, 62, 68, 89]), array([94, 62, 68, 89]))

# %% same-seed-loop
for _ in range(3):
    print(np.random.default_rng(1).integers(0, 100))   # новый генератор с тем же seed — одно и то же
# ─── вывод ───
# 47
# 47
# 47

# %% legacy
np.random.seed(42)
print(np.random.rand(3))        # старый API: работает, но числа другие
np.random.default_rng(42).random(3)
# ─── вывод ───
# [0.37454012 0.95071431 0.73199394]
# array([0.77395605, 0.43887844, 0.85859792])

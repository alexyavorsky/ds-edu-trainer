# Примеры к статье numpy/vectorization.

# %% setup
import timeit

rng = np.random.default_rng(0)
amounts = rng.uniform(100, 5000, size=100_000)   # суммы покупок

def bonus_vector(values):                        # бонус 5 % с покупок дороже 1000
    return np.where(values > 1000, values * 0.05, 0.0)

# %% loop-vs-vector [timing=2026-09-29, machine=Apple M4 · macOS · Python 3.14]
def bonus_loop(values):
    result = []
    for v in values:
        result.append(v * 0.05 if v > 1000 else 0.0)
    return np.array(result)

print(np.allclose(bonus_loop(amounts), bonus_vector(amounts)))   # результат одинаковый, а время — нет
t_loop = min(timeit.repeat(lambda: bonus_loop(amounts), number=1, repeat=5))
t_vector = min(timeit.repeat(lambda: bonus_vector(amounts), number=1, repeat=5))
print(f"цикл: {t_loop * 1000:.1f} мс, векторно: {t_vector * 1000:.2f} мс")
print(f"ускорение: ×{t_loop / t_vector:.0f}")
# ─── вывод ───
# True
# цикл: 6.4 мс, векторно: 0.06 мс
# ускорение: ×112

# %% cumulative
# «Сколько потрачено к каждой покупке» — не цикл с суммой, а cumsum
day = np.array([300.0, 150.0, 700.0, 50.0])
np.cumsum(day)
# ─── вывод ───
# array([ 300.,  450., 1150., 1200.])

# %% conditions
# цикл с if/elif превращается в np.select
tier = np.select([amounts < 500, amounts < 2000], ["малая", "средняя"], default="крупная")
tier[:5]
# ─── вывод ───
# array(['крупная', 'средняя', 'малая', 'малая', 'крупная'], dtype='<U7')

# %% pairwise
# двойной цикл «каждый с каждым» — транслирование
points = np.array([[0.0, 0.0], [3.0, 4.0], [6.0, 8.0]])
diff = points[:, np.newaxis, :] - points[np.newaxis, :, :]
np.sqrt((diff ** 2).sum(axis=-1))                                 # матрица расстояний
# ─── вывод ───
# array([[ 0.,  5., 10.],
#        [ 5.,  0.,  5.],
#        [10.,  5.,  0.]])

# %% np-vectorize [timing=2026-09-29, machine=Apple M4 · macOS · Python 3.14]
def bonus_one(v):
    return v * 0.05 if v > 1000 else 0.0

bonus_vectorized = np.vectorize(bonus_one)
print(np.allclose(bonus_vectorized(amounts), bonus_vector(amounts)))
t_vectorize = min(timeit.repeat(lambda: bonus_vectorized(amounts), number=1, repeat=5))
t_vector = min(timeit.repeat(lambda: bonus_vector(amounts), number=1, repeat=5))
print(f"np.vectorize: {t_vectorize * 1000:.1f} мс, np.where: {t_vector * 1000:.2f} мс")
print(f"np.where быстрее: ×{t_vectorize / t_vector:.0f}")   # np.vectorize — тот же цикл внутри
# ─── вывод ───
# True
# np.vectorize: 5.8 мс, np.where: 0.06 мс
# np.where быстрее: ×101

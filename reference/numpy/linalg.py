# Примеры к статье numpy/linalg.
# Результаты округлены: в последних знаках они зависят от библиотеки BLAS на машине.

# %% setup
# 2 билета взрослых и 1 детский стоят 950, 1 взрослый и 3 детских — 1100
A = np.array([[2.0, 1.0],
              [1.0, 3.0]])
b = np.array([950.0, 1100.0])
M = np.array([[1.0, 2.0],
              [2.0, 4.0]])                 # вырожденная: вторая строка = первая × 2

# %% solve
np.linalg.solve(A, b).round(6)             # цены: взрослый и детский
# ─── вывод ───
# array([350., 250.])

# %% inv-det
print(np.linalg.inv(A).round(6))
np.linalg.det(A).round(6)
# ─── вывод ───
# [[ 0.6 -0.2]
#  [-0.2  0.4]]
# np.float64(5.0)

# %% solve-vs-inv
x1 = np.linalg.solve(A, b)
x2 = np.linalg.inv(A) @ b                  # работает, но медленнее и менее точно
np.allclose(x1, x2)
# ─── вывод ───
# True

# %% norm
v = np.array([3.0, 4.0])
print(np.linalg.norm(v))                   # длина вектора
print(np.linalg.norm(v, ord=1))            # сумма модулей
np.linalg.norm(A, axis=1).round(6)         # длина каждой строки
# ─── вывод ───
# 5.0
# 7.0
# array([2.236068, 3.162278])

# %% eigh
values, vectors = np.linalg.eigh(A)        # для симметричных матриц
values.round(6)
# ─── вывод ───
# array([1.381966, 3.618034])

# %% eig-complex
values, vectors = np.linalg.eig(A)         # общий случай: порядок значений не гарантирован
np.sort(values).round(6)                   # с NumPy 2.5 всегда комплексные
# ─── вывод ───
# array([1.381966+0.j, 3.618034+0.j])

# %% lstsq
hours = np.array([1.0, 2.0, 3.0, 4.0])
score = np.array([52.0, 55.0, 61.0, 64.0])
X = np.column_stack([np.ones(4), hours])   # столбец единиц — свободный член
coef, *_ = np.linalg.lstsq(X, score)
coef.round(6)                              # score ≈ coef[0] + coef[1] * hours
# ─── вывод ───
# array([47.5,  4.2])

# %% rank
np.linalg.matrix_rank(M)
# ─── вывод ───
# np.int64(1)

# %% singular [raises=LinAlgError]
np.linalg.solve(M, b)
# ─── вывод ───
# LinAlgError: Singular matrix

# Примеры к статье numpy/broadcasting.
# Вывод под примерами пишет scripts/validate_reference.py --update — руками не править.

# %% setup
# оценки трёх учеников по четырём предметам
scores = np.array([[4, 5, 3, 4],
                   [5, 5, 4, 3],
                   [3, 5, 5, 5]])

# %% scalar
prices = np.array([120.0, 80.0, 45.0])
prices * 0.9
# ─── вывод ───
# array([108. ,  72. ,  40.5])

# %% row
subject_mean = scores.mean(axis=0)   # форма (4,) — среднее по каждому предмету
print(subject_mean)
scores - subject_mean                # (3, 4) и (4,) → (3, 4)
# ─── вывод ───
# [4. 5. 4. 4.]
# array([[ 0.,  0., -1.,  0.],
#        [ 1.,  0.,  0., -1.],
#        [-1.,  0.,  1.,  1.]])

# %% column
student_mean = scores.mean(axis=1, keepdims=True)   # форма (3, 1)
print(student_mean)
scores - student_mean                                # (3, 4) и (3, 1) → (3, 4)
# ─── вывод ───
# [[4.  ]
#  [4.25]
#  [4.5 ]]
# array([[ 0.  ,  1.  , -1.  ,  0.  ],
#        [ 0.75,  0.75, -0.25, -1.25],
#        [-1.5 ,  0.5 ,  0.5 ,  0.5 ]])

# %% outer
prices = np.array([120, 80, 45])      # три товара
qty = np.array([1, 2, 5, 10])         # варианты количества
prices[:, np.newaxis] * qty           # (3, 1) и (4,) → (3, 4)
# ─── вывод ───
# array([[ 120,  240,  600, 1200],
#        [  80,  160,  400,  800],
#        [  45,   90,  225,  450]])

# %% shapes
print(np.broadcast_shapes((3, 1), (4,)))
print(np.broadcast_shapes((2, 3, 4), (3, 4)))
np.broadcast_shapes((8, 1, 6, 1), (7, 1, 5))
# ─── вывод ───
# (3, 4)
# (2, 3, 4)
# (8, 7, 6, 5)

# %% mismatch [raises=ValueError]
scores - scores.mean(axis=1)          # (3, 4) и (3,): 4 ≠ 3
# ─── вывод ───
# ValueError: operands could not be broadcast together with shapes (3,4) (3,)

# %% silent
square = np.array([[1, 2, 3],
                   [4, 5, 6],
                   [7, 8, 9]])
row_mean = square.mean(axis=1)                  # форма (3,)
print(square - row_mean)                        # молча вычтено по столбцам!
square - square.mean(axis=1, keepdims=True)     # правильно: по строкам
# ─── вывод ───
# [[-1. -3. -5.]
#  [ 2.  0. -2.]
#  [ 5.  3.  1.]]
# array([[-1.,  0.,  1.],
#        [-1.,  0.,  1.],
#        [-1.,  0.,  1.]])

# %% readonly [raises=ValueError]
grid = np.broadcast_to(np.array([1, 2, 3]), (2, 3))
print(grid)
grid[0, 0] = 10
# ─── вывод ───
# [[1 2 3]
#  [1 2 3]]
# ValueError: assignment destination is read-only

# %% inplace [raises=ValueError]
total = np.zeros(3)
total += np.ones((2, 3))   # результат (2, 3) не помещается в массив формы (3,)
# ─── вывод ───
# ValueError: non-broadcastable output operand with shape (3,) doesn't match the broadcast shape (2,3)

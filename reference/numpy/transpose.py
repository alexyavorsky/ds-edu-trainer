# Примеры к статье numpy/transpose.

# %% setup
# оценки: 2 ученика × 3 предмета
scores = np.array([[4, 5, 3],
                   [5, 4, 4]])

# %% t
print(scores.T)          # 3 предмета × 2 ученика
scores.T.shape
# ─── вывод ───
# [[4 5]
#  [5 4]
#  [3 4]]
# (3, 2)

# %% transpose-axes
batch = np.zeros((10, 28, 28, 3))              # картинки × высота × ширина × каналы
print(np.transpose(batch, (0, 3, 1, 2)).shape) # каналы на второе место
print(np.moveaxis(batch, -1, 1).shape)         # то же через moveaxis
np.swapaxes(batch, 1, 2).shape
# ─── вывод ───
# (10, 3, 28, 28)
# (10, 3, 28, 28)
# (10, 28, 28, 3)

# %% newaxis
v = np.array([1, 2, 3])
print(v[np.newaxis, :].shape)   # строка (1, 3)
print(v[:, np.newaxis].shape)   # столбец (3, 1)
np.expand_dims(v, axis=1).shape
# ─── вывод ───
# (1, 3)
# (3, 1)
# (3, 1)

# %% squeeze
col = np.array([[7], [8], [9]])   # (3, 1)
print(np.squeeze(col))
np.zeros((1, 5, 1)).squeeze().shape
# ─── вывод ───
# [7 8 9]
# (5,)

# %% vector-t
v = np.array([1, 2, 3])
v.T.shape                          # у одномерного массива транспонирование ничего не меняет
# ─── вывод ───
# (3,)

# %% squeeze-error [raises=ValueError]
np.zeros((3, 2)).squeeze(axis=1)   # ось длины 2 убрать нельзя
# ─── вывод ───
# ValueError: cannot select an axis to squeeze out which has size not equal to one

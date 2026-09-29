# Примеры к статье numpy/memory-layout.

# %% setup
m = np.arange(12, dtype=np.int64).reshape(3, 4)

# %% strides
print(m.strides)          # байт до следующей строки и до следующего столбца
m.T.strides               # транспонирование только меняет strides местами
# ─── вывод ───
# (32, 8)
# (8, 32)

# %% flags
print(m.flags["C_CONTIGUOUS"], m.flags["F_CONTIGUOUS"])
m.T.flags["C_CONTIGUOUS"], m.T.flags["F_CONTIGUOUS"]
# ─── вывод ───
# True False
# (False, True)

# %% order-f
f = np.asfortranarray(m)  # те же значения, в памяти по столбцам
print(f.strides)
np.array_equal(f, m)
# ─── вывод ───
# (8, 24)
# True

# %% slice-strides
every_other = m[:, ::2]
print(every_other.strides)                 # шаг по столбцам вдвое больше
every_other.flags["C_CONTIGUOUS"]          # данные идут с пропусками
# ─── вывод ───
# (32, 16)
# False

# %% contiguous
c = np.ascontiguousarray(m.T)              # копия в порядке C
c.flags["C_CONTIGUOUS"], np.shares_memory(c, m)
# ─── вывод ───
# (True, False)

# %% ravel-copy
print(np.shares_memory(m.ravel(), m))      # C-массив вытягивается без копии
np.shares_memory(m.T.ravel(), m)           # транспонированный — только с копией
# ─── вывод ───
# True
# False

# Примеры к статье numpy/indexing.

# %% setup
# дневная выручка за неделю, пн–вс
revenue = np.array([120, 95, 130, 110, 160, 210, 180])

# %% single
print(revenue[0])     # понедельник
print(revenue[-1])    # последний элемент — воскресенье
revenue[-2]
# ─── вывод ───
# 120
# 180
# np.int64(210)

# %% slices
print(revenue[1:4])   # вт, ср, чт — stop не входит
print(revenue[:5])    # будни
revenue[5:]           # выходные
# ─── вывод ───
# [ 95 130 110]
# [120  95 130 110 160]
# array([210, 180])

# %% step
print(revenue[::2])   # каждый второй день
revenue[::-1]         # в обратном порядке
# ─── вывод ───
# [120 130 160 180]
# array([180, 210, 160, 110, 130,  95, 120])

# %% assign
revenue[5:] = 0       # число записывается во все элементы среза
print(revenue)
revenue[:3] = [1, 2, 3]
revenue
# ─── вывод ───
# [120  95 130 110 160   0   0]
# array([  1,   2,   3, 110, 160,   0,   0])

# %% view
weekend = revenue[5:]
weekend[:] = 0        # меняем срез…
revenue               # …и меняется исходный массив
# ─── вывод ───
# array([120,  95, 130, 110, 160,   0,   0])

# %% out-of-range [raises=IndexError]
print(revenue[5:100])  # срез за границей — просто короче
revenue[7]
# ─── вывод ───
# [210 180]
# IndexError: index 7 is out of bounds for axis 0 with size 7

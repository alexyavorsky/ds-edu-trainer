# Примеры к статье numpy/comparing.

# %% setup
plan = np.array([100, 120, 90])   # план продаж
fact = np.array([100, 115, 95])   # факт

# %% elementwise
print(plan == fact)
fact >= plan
# ─── вывод ───
# [ True False False]
# array([ True, False,  True])

# %% if-array [raises=ValueError]
if plan == fact:
    print("план выполнен")
# ─── вывод ───
# ValueError: The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()

# %% array-equal
print(np.array_equal(plan, fact))
print(np.array_equal(plan, [100, 120, 90]))
np.array_equal(plan, [100, 120])          # другая форма — просто False
# ─── вывод ───
# False
# True
# False

# %% floats
x = np.array([0.1 + 0.2, 1 / 3 * 3])
print(x == np.array([0.3, 1.0]))
print(np.isclose(x, [0.3, 1.0]))
np.allclose(x, [0.3, 1.0])
# ─── вывод ───
# [False  True]
# [ True  True]
# True

# %% tolerance
measured = np.array([9.98, 20.03])
print(np.allclose(measured, [10, 20]))              # по умолчанию допуск очень мал
np.allclose(measured, [10, 20], atol=0.05)
# ─── вывод ───
# False
# True

# %% nan
a = np.array([1.0, np.nan])
print(a == a)
print(np.array_equal(a, a))
np.array_equal(a, a, equal_nan=True)
# ─── вывод ───
# [ True False]
# False
# True

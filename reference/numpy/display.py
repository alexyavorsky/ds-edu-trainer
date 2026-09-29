# Примеры к статье numpy/display.

# %% print-vs-repr
a = np.array([1.5, 2, 3])
print(a)          # print — для людей
a                 # repr — как это записать в коде
# ─── вывод ───
# [1.5 2.  3. ]
# array([1.5, 2. , 3. ])

# %% scalar
x = np.float64(0.1) * 3
print(x)
x
# ─── вывод ───
# 0.30000000000000004
# np.float64(0.30000000000000004)

# %% precision
thirds = np.array([1 / 3, 2 / 3, 1.0])
with np.printoptions(precision=3):
    print(thirds)
print(thirds)     # вне блока with — снова как обычно
# ─── вывод ───
# [0.333 0.667 1.   ]
# [0.33333333 0.66666667 1.        ]

# %% suppress
values = np.array([0.00001, 1.5, 2500.0])
print(values)
with np.printoptions(suppress=True):
    print(values)
# ─── вывод ───
# [1.0e-05 1.5e+00 2.5e+03]
# [   0.00001    1.5     2500.     ]

# %% threshold
np.arange(2000)   # больше 1000 элементов — показываются только края
# ─── вывод ───
# array([   0,    1,    2, ..., 1997, 1998, 1999], shape=(2000,))

# %% display-only
prices = np.array([10.123, 20.456])
with np.printoptions(precision=1):
    print(prices)
    print(prices.sum())   # скаляр печатается полностью
prices[0]                 # данные не округлены
# ─── вывод ───
# [10.1 20.5]
# 30.579
# np.float64(10.123)

# %% legacy
with np.printoptions(legacy="1.25"):
    print(repr(np.float64(0.5)))
# ─── вывод ───
# 0.5

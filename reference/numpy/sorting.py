# Примеры к статье numpy/sorting.

# %% setup
prices = np.array([480, 120, 310, 90, 250])
names = np.array(["чайник", "кружка", "тостер", "ложка", "миска"])

# %% sort
print(np.sort(prices))                    # новый массив
np.sort(prices, descending=True)          # по убыванию (NumPy 2.5)
# ─── вывод ───
# [ 90 120 250 310 480]
# array([480, 310, 250, 120,  90])

# %% in-place
copy = prices.copy()
result = copy.sort()                      # метод сортирует на месте…
print(result)                             # …и возвращает None
copy
# ─── вывод ───
# None
# array([ 90, 120, 250, 310, 480])

# %% argsort
order = np.argsort(prices)                # индексы в порядке возрастания цены
print(order)
names[order]                              # упорядочить другой массив так же
# ─── вывод ───
# [3 1 4 2 0]
# array(['ложка', 'кружка', 'миска', 'тостер', 'чайник'], dtype='<U6')

# %% axis
m = np.array([[3, 8, 2],
              [9, 1, 5]])
print(np.sort(m))                         # каждая строка (axis=-1)
np.sort(m, axis=0)                        # каждый столбец
# ─── вывод ───
# [[2 3 8]
#  [1 5 9]]
# array([[3, 1, 2],
#        [9, 8, 5]])

# %% rows-by-column
table = np.array([[3, 250],
                  [1, 480],
                  [2, 120]])              # столбцы: id, цена
table[table[:, 1].argsort()]              # строки по второму столбцу
# ─── вывод ───
# array([[  2, 120],
#        [  3, 250],
#        [  1, 480]])

# %% lexsort
city = np.array(["Тула", "Омск", "Тула", "Омск"])
score = np.array([7, 9, 5, 9])
idx = np.lexsort((score, city))           # главный ключ — ПОСЛЕДНИЙ
city[idx], score[idx]
# ─── вывод ───
# (array(['Омск', 'Омск', 'Тула', 'Тула'], dtype='<U4'), array([9, 9, 5, 7]))

# %% reverse-old
np.sort(prices)[::-1]                     # старый способ «по убыванию»
# ─── вывод ───
# array([480, 310, 250, 120,  90])

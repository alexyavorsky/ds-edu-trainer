# Примеры к статье numpy/strings.

# %% setup
cities = np.array(["  москва", "Тула ", "омск"])
codes = np.array(["SKU-101", "SKU-202", "BOX-303"])

# %% functions
clean = np.strings.strip(cities)
print(clean)
print(np.strings.capitalize(clean))
np.strings.str_len(clean)
# ─── вывод ───
# ['москва' 'Тула' 'омск']
# ['Москва' 'Тула' 'Омск']
# array([6, 4, 4])

# %% search
print(np.strings.startswith(codes, "SKU"))
print(np.strings.find(codes, "-"))
np.strings.replace(codes, "SKU", "ART")
# ─── вывод ───
# [ True  True False]
# [3 3 3]
# array(['ART-101', 'ART-202', 'BOX-303'], dtype='<U7')

# %% slice
np.strings.slice(codes, 4, None)             # символы с 4-го
# ─── вывод ───
# array(['101', '202', '303'], dtype='<U7')

# %% stringdtype
names = np.array(["Аня", "Борис"], dtype=np.dtypes.StringDType())
names[0] = "Анастасия"                        # длина не ограничена
names
# ─── вывод ───
# array(['Анастасия', 'Борис'], dtype=StringDType())

# %% fixed-width
names = np.array(["Аня", "Борис"])            # dtype <U5 — не больше 5 символов
print(names.dtype)
names[0] = "Анастасия"
names                                         # строка молча обрезана
# ─── вывод ───
# <U5
# array(['Анаст', 'Борис'], dtype='<U5')

# %% char-legacy
np.char.upper(np.array(["a", "b"]))           # старый модуль: работает, но в новом коде — np.strings
# ─── вывод ───
# array(['A', 'B'], dtype='<U1')

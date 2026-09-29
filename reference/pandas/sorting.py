# Примеры к статье pandas/sorting.

# %% setup
staff = pd.DataFrame({
    "name": ["Вика", "аня", "Борис", "Глеб", "Дина"],
    "dept": ["IT", "HR", "IT", "HR", "IT"],
    "salary": [95, 60, 120, None, 95],
})

# %% by-column
staff.sort_values("salary")                       # пропуски — в конце
# ─── вывод ───
#     name dept  salary
# 1    аня   HR    60.0
# 0   Вика   IT    95.0
# 4   Дина   IT    95.0
# 2  Борис   IT   120.0
# 3   Глеб   HR     NaN

# %% descending
staff.sort_values("salary", ascending=False)
# ─── вывод ───
#     name dept  salary
# 2  Борис   IT   120.0
# 0   Вика   IT    95.0
# 4   Дина   IT    95.0
# 1    аня   HR    60.0
# 3   Глеб   HR     NaN

# %% several
staff.sort_values(["dept", "salary"], ascending=[True, False])   # отдел по алфавиту, зарплата по убыванию
# ─── вывод ───
#     name dept  salary
# 1    аня   HR    60.0
# 3   Глеб   HR     NaN
# 2  Борис   IT   120.0
# 0   Вика   IT    95.0
# 4   Дина   IT    95.0

# %% key
staff.sort_values("name", key=lambda s: s.str.lower())           # без учёта регистра
# ─── вывод ───
#     name dept  salary
# 1    аня   HR    60.0
# 2  Борис   IT   120.0
# 0   Вика   IT    95.0
# 3   Глеб   HR     NaN
# 4   Дина   IT    95.0

# %% ignore-index
staff.sort_values("salary", na_position="first", ignore_index=True)
# ─── вывод ───
#     name dept  salary
# 0   Глеб   HR     NaN
# 1    аня   HR    60.0
# 2   Вика   IT    95.0
# 3   Дина   IT    95.0
# 4  Борис   IT   120.0

# %% sort-index
staff.sort_values("salary").sort_index()          # вернуть исходный порядок строк
# ─── вывод ───
#     name dept  salary
# 0   Вика   IT    95.0
# 1    аня   HR    60.0
# 2  Борис   IT   120.0
# 3   Глеб   HR     NaN
# 4   Дина   IT    95.0

# %% nlargest
staff.nlargest(2, "salary")                       # две наибольшие зарплаты
# ─── вывод ───
#     name dept  salary
# 2  Борис   IT   120.0
# 0   Вика   IT    95.0

# %% not-inplace
staff.sort_values("salary")                       # результат не сохранён…
staff.head(2)                                     # …таблица осталась прежней
# ─── вывод ───
#    name dept  salary
# 0  Вика   IT    95.0
# 1   аня   HR    60.0

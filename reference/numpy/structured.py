# Примеры к статье numpy/structured.

# %% setup
student = np.dtype([("name", "U10"), ("age", "i4"), ("score", "f8")])
people = np.array([("Аня", 21, 4.5),
                   ("Борис", 19, 3.8),
                   ("Вика", 22, 4.9)], dtype=student)

# %% create
print(people.dtype)
people
# ─── вывод ───
# [('name', '<U10'), ('age', '<i4'), ('score', '<f8')]
# array([('Аня', 21, 4.5), ('Борис', 19, 3.8), ('Вика', 22, 4.9)],
#       dtype=[('name', '<U10'), ('age', '<i4'), ('score', '<f8')])

# %% field
print(people["name"])
people["score"].mean()
# ─── вывод ───
# ['Аня' 'Борис' 'Вика']
# np.float64(4.4)

# %% row
print(people[1])
people[1]["age"]
# ─── вывод ───
# ('Борис', 19, 3.8)
# np.int32(19)

# %% filter
people[people["score"] > 4]["name"]
# ─── вывод ───
# array(['Аня', 'Вика'], dtype='<U10')

# %% sort
np.sort(people, order="age")["name"]
# ─── вывод ───
# array(['Борис', 'Аня', 'Вика'], dtype='<U10')

# %% assign
people["age"] += 1
people["age"]
# ─── вывод ───
# array([22, 20, 23], dtype=int32)

# %% to-pandas
pd.DataFrame(people)                    # для анализа таблиц удобнее pandas
# ─── вывод ───
#     name  age  score
# 0    Аня   21    4.5
# 1  Борис   19    3.8
# 2   Вика   22    4.9

# %% truncate
people["name"][0] = "Александра-Мария"    # 16 символов в поле U10
people["name"]
# ─── вывод ───
# array(['Александра', 'Борис', 'Вика'], dtype='<U10')

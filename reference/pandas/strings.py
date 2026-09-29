# Примеры к статье pandas/strings.

# %% setup
clients = pd.DataFrame({
    "name": ["  анна ПЕТРОВА", "Борис Иванов ", "вика сидорова", None],
    "email": ["anna@mail.ru", "boris@yandex.ru", "vika@mail.ru", "x@gmail.com"],
    "phone": ["+7 (912) 345-67-89", "8-912-111-22-33", "89125554433", "—"],
})

# %% clean
clients["name"].str.strip().str.title()
# ─── вывод ───
# 0     Анна Петрова
# 1     Борис Иванов
# 2    Вика Сидорова
# 3              NaN
# Name: name, dtype: str

# %% contains
clients[clients["email"].str.contains("mail.ru", regex=False)]
# ─── вывод ───
#              name         email               phone
# 0    анна ПЕТРОВА  anna@mail.ru  +7 (912) 345-67-89
# 2   вика сидорова  vika@mail.ru         89125554433

# %% startswith
clients["email"].str.endswith("@mail.ru")
# ─── вывод ───
# 0     True
# 1    False
# 2     True
# 3    False
# Name: email, dtype: bool

# %% split
clients["name"].str.strip().str.split(" ", expand=True)   # в отдельные столбцы
# ─── вывод ───
#        0         1
# 0   анна   ПЕТРОВА
# 1  Борис    Иванов
# 2   вика  сидорова
# 3    NaN       NaN

# %% extract
clients["email"].str.extract(r"@(\w+)\.")                 # группа регулярного выражения
# ─── вывод ───
#         0
# 0    mail
# 1  yandex
# 2    mail
# 3   gmail

# %% replace
clients["phone"].str.replace(r"\D", "", regex=True)       # оставить только цифры
# ─── вывод ───
# 0    79123456789
# 1    89121112233
# 2    89125554433
# 3
# Name: phone, dtype: str

# %% len-slice
print(clients["email"].str.len().tolist())
clients["email"].str[:4]                                   # первые 4 символа
# ─── вывод ───
# [12, 15, 12, 11]
# 0    anna
# 1    bori
# 2    vika
# 3    x@gm
# Name: email, dtype: str

# %% cat
clients["name"].str.strip().str.cat(sep=", ")              # склеить значения столбца
# ─── вывод ───
# 'анна ПЕТРОВА, Борис Иванов, вика сидорова'

# %% na
print(clients["name"].str.upper().tolist())                # пропуск остаётся пропуском
clients["name"].str.contains("ов").tolist()                # а у contains для пропуска — False
# ─── вывод ───
# ['  АННА ПЕТРОВА', 'БОРИС ИВАНОВ ', 'ВИКА СИДОРОВА', nan]
# [False, True, True, False]

# %% regex-default
clients["email"].str.contains(".ru").tolist()              # «.» в регулярном выражении — любой символ
# ─── вывод ───
# [True, True, True, False]

# %% no-str [raises=AttributeError]
pd.Series([1, 2]).str.len()                                # .str только для строк
# ─── вывод ───
# AttributeError: Can only use .str accessor with string values, not integer

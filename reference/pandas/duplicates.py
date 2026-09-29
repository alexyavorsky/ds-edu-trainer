# Примеры к статье pandas/duplicates.

# %% setup
visits = pd.DataFrame({
    "user": ["ann", "bob", "ann", "kate", "bob", "ann"],
    "page": ["/home", "/cart", "/home", "/home", "/pay", "/cart"],
    "time": ["10:00", "10:02", "10:05", "10:06", "10:07", "10:09"],
})

# %% duplicated
visits.duplicated(subset=["user", "page"])        # True — повтор уже встречавшейся пары
# ─── вывод ───
# 0    False
# 1    False
# 2     True
# 3    False
# 4    False
# 5    False
# dtype: bool

# %% count
visits.duplicated(subset=["user", "page"]).sum()
# ─── вывод ───
# np.int64(1)

# %% drop
visits.drop_duplicates(subset=["user", "page"])   # оставить первое вхождение
# ─── вывод ───
#    user   page   time
# 0   ann  /home  10:00
# 1   bob  /cart  10:02
# 3  kate  /home  10:06
# 4   bob   /pay  10:07
# 5   ann  /cart  10:09

# %% keep-last
visits.drop_duplicates(subset="user", keep="last")   # последнее посещение каждого пользователя
# ─── вывод ───
#    user   page   time
# 3  kate  /home  10:06
# 4   bob   /pay  10:07
# 5   ann  /cart  10:09

# %% keep-false
visits[visits.duplicated(subset="user", keep=False)]   # все строки пользователей с повторами
# ─── вывод ───
#   user   page   time
# 0  ann  /home  10:00
# 1  bob  /cart  10:02
# 2  ann  /home  10:05
# 4  bob   /pay  10:07
# 5  ann  /cart  10:09

# %% whole-row
visits.duplicated().sum()                         # без subset сравниваются все столбцы
# ─── вывод ───
# np.int64(0)

# %% ignore-index
visits.drop_duplicates(subset="user", ignore_index=True)
# ─── вывод ───
#    user   page   time
# 0   ann  /home  10:00
# 1   bob  /cart  10:02
# 2  kate  /home  10:06

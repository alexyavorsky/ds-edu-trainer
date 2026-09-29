# Примеры к статье pandas/replace.

# %% setup
survey = pd.DataFrame({
    "city": ["Спб", "Москва", "С.-Петербург", "мск", "Москва"],
    "answer": ["да", "нет", "н/д", "да", "-"],
    "score": [5, -1, 4, 3, -1],        # -1 — «нет ответа»
})

# %% scalar
survey["score"].replace(-1, np.nan)
# ─── вывод ───
# 0    5.0
# 1    NaN
# 2    4.0
# 3    3.0
# 4    NaN
# Name: score, dtype: float64

# %% dict
survey["city"].replace({"Спб": "Санкт-Петербург", "С.-Петербург": "Санкт-Петербург", "мск": "Москва"})
# ─── вывод ───
# 0    Санкт-Петербург
# 1             Москва
# 2    Санкт-Петербург
# 3             Москва
# 4             Москва
# Name: city, dtype: str

# %% list
survey.replace(["н/д", "-"], np.nan)          # несколько значений — в одно
# ─── вывод ───
#            city answer  score
# 0           Спб     да      5
# 1        Москва    нет     -1
# 2  С.-Петербург    NaN      4
# 3           мск     да      3
# 4        Москва    NaN     -1

# %% per-column
survey.replace({"answer": {"да": "yes", "нет": "no"}, "score": {-1: 0}})
# ─── вывод ───
#            city answer  score
# 0           Спб    yes      5
# 1        Москва     no      0
# 2  С.-Петербург    н/д      4
# 3           мск    yes      3
# 4        Москва      -      0

# %% regex
survey["city"].replace(r"^С.*[Пп]етербург$|^Спб$", "Санкт-Петербург", regex=True)
# ─── вывод ───
# 0    Санкт-Петербург
# 1             Москва
# 2    Санкт-Петербург
# 3                мск
# 4             Москва
# Name: city, dtype: str

# %% whole-value
print(survey["city"].replace("Москва", "МСК").tolist())   # только целое значение
survey["city"].str.replace("о", "0").tolist()             # подстрока — это .str.replace
# ─── вывод ───
# ['Спб', 'МСК', 'С.-Петербург', 'мск', 'МСК']
# ['Спб', 'М0сква', 'С.-Петербург', 'мск', 'М0сква']

# %% vs-map
codes = {"да": 1, "нет": 0}
print(survey["answer"].replace(codes).tolist())   # незнакомые значения остаются
survey["answer"].map(codes).tolist()              # незнакомые — NaN
# ─── вывод ───
# [1, 0, 'н/д', 1, '-']
# [1.0, 0.0, nan, 1.0, nan]

# %% inplace
result = survey.replace(-1, 0, inplace=True)
result is survey                                   # pandas 3: inplace возвращает саму таблицу
# ─── вывод ───
# True

# Примеры к статье pandas/plot.
# Графики строятся без окон (matplotlib с бэкендом Agg); валидатор сохраняет каждую фигуру в SVG,
# и статья показывает её вместо объекта осей, который вернул .plot.

# %% setup
sales = pd.DataFrame(
    {"latte": [120, 135, 150, 142], "tea": [80, 70, 65, 90]},
    index=pd.Index(["янв", "фев", "мар", "апр"], name="month"),
)

# %% line
sales.plot(title="Продажи по месяцам")                  # линии: по одной на столбец

# %% bar
sales.plot.bar(rot=0)                                   # или kind="bar"

# %% one-column
sales["latte"].plot.barh(color="tab:orange")

# %% hist
rng = np.random.default_rng(1)
pd.Series(rng.normal(170, 8, 500)).plot.hist(bins=20)

# %% scatter
sales.plot.scatter(x="latte", y="tea")

# %% save
ax = sales.plot.area(alpha=0.5)
ax.set_ylabel("чашек")
ax.figure.savefig("sales.png", dpi=120)                 # сохранить в файл

# %% no-numeric [raises=TypeError]
pd.DataFrame({"month": ["янв", "фев"], "cups": ["120", "135"]}).plot()   # числа прочитаны как текст
# ─── вывод ───
# TypeError: no numeric data to plot

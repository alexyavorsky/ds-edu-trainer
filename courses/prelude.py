# Выполняется в начале каждого сеанса урока (на сайте не показывается), в отдельном пространстве имён:
# импорты отсюда уроку не видны — урок импортирует numpy и pandas сам. Настройки заданы явно, чтобы вывод
# не зависел от окна и машины: без них pandas подстраивает число столбцов под ширину терминала.
# Блок пакета выполняется, только если пакет загружен (урок NumPy не тянет pandas).
import numpy as np

np.set_printoptions(linewidth=75, precision=8, threshold=1000, edgeitems=3)

import pandas as pd

pd.set_option("display.width", 80)
pd.set_option("display.max_columns", 20)
pd.set_option("display.max_rows", 60)
pd.set_option("display.min_rows", 10)
pd.set_option("display.max_colwidth", 50)

import matplotlib

matplotlib.use("Agg")

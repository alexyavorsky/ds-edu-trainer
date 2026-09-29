# Выполняется перед каждым примером справочника (на сайте не показывается).
# Настройки заданы явно, чтобы вывод не зависел от терминала и машины:
# без них pandas подстраивает число столбцов под ширину окна.
import numpy as np
import pandas as pd

np.set_printoptions(linewidth=75, precision=8, threshold=1000, edgeitems=3)
pd.set_option("display.width", 80)
pd.set_option("display.max_columns", 20)
pd.set_option("display.max_rows", 60)
pd.set_option("display.min_rows", 10)
pd.set_option("display.max_colwidth", 50)
pd.set_option("display.precision", 6)

import matplotlib

matplotlib.use("Agg")  # графики строятся без окон; валидатор сохраняет их в SVG для статьи

"""Выполнение примера справочника как ячейки Jupyter — общее для валидатора и сайта.

Этот модуль импортирует scripts/validate_reference.py, и он же выполняет примеры в браузере (Pyodide),
поэтому вывод на сайте получается тем же способом, что и сохранённый в статье:

- перед примером выполняются reference/prelude.py и setup статьи, пространство имён у каждого примера своё;
- печатается stdout (и stderr), затем repr последнего выражения (если не None);
- предупреждения выводятся строкой «Категория: текст», исключение — последней строкой «Тип: текст»;
- у каждого примера своя пустая временная рабочая папка;
- фигуры matplotlib, оставшиеся открытыми, сохраняются в SVG в цветах сайта; объект осей в текстовый
  вывод не попадает — вместо него показывается график.

prelude.py выполняется частями — по импортам: блок «import pandas as pd» и настройки после него
выполняются, только если pandas доступен. Валидатору доступно всё; в браузере статья NumPy не загружает
pandas и matplotlib, пока пример их не использует.
"""

from __future__ import annotations

import ast
import contextlib
import importlib.util
import io
import os
import sys
import tempfile
import warnings
from dataclasses import dataclass, field

# Графики в цветах сайта (src/styles/global.css): прозрачный фон ложится на блок вывода.
PLOT_RC = {
    "figure.figsize": (6.4, 3.6),
    "figure.facecolor": "none",
    "axes.facecolor": "none",
    "savefig.facecolor": "none",
    "savefig.bbox": "tight",
    "axes.edgecolor": "#2d3036",
    "axes.labelcolor": "#b7bac1",
    "axes.titlecolor": "#f4f5f6",
    "axes.prop_cycle": ["#8d95ff", "#4cc38a", "#eeb153", "#f07a7d", "#5ec8e5", "#c792ea"],  # цвета линий
    "xtick.color": "#8a8f98",
    "ytick.color": "#8a8f98",
    "grid.color": "#2d3036",
    "text.color": "#b7bac1",
    "legend.facecolor": "#141518",
    "legend.edgecolor": "#2d3036",
    "legend.labelcolor": "#b7bac1",
    "patch.edgecolor": "#08090a",
    "font.family": "sans-serif",   # в SVG: 'DejaVu Sans', sans-serif — без шрифта браузер возьмёт рубленый
    "font.sans-serif": ["DejaVu Sans"],  # идёт с matplotlib: разметка текста одинакова на любой машине
    "svg.fonttype": "none",        # текст остаётся текстом: файл меньше, подписи чёткие
    "svg.hashsalt": "reference",   # иначе id элементов в SVG случайные
}


@dataclass
class RunResult:
    lines: list[str]
    error: BaseException | None
    categories: list[type]  # категории предупреждений
    plots: list[str]  # SVG открытых после примера фигур matplotlib
    error_line: int | None = None  # строка примера, где возникло исключение
    truncated: bool = False  # вывод обрезан по лимиту
    packages: list[str] = field(default_factory=list)  # пакеты, чьи блоки prelude выполнены


class LimitedOutput(io.StringIO):
    """Буфер вывода; сверх лимита (символы или строки) текст отбрасывается — бесконечный print не съест память."""

    def __init__(self, max_chars: int | None = None, max_lines: int | None = None):
        super().__init__()
        self.max_chars, self.max_lines = max_chars, max_lines
        self.chars = self.lines = 0
        self.truncated = False

    def write(self, text: str) -> int:
        size = len(text)
        if self.truncated:
            return size
        if self.max_lines is not None and self.lines + text.count("\n") > self.max_lines:
            keep = self.max_lines - self.lines
            text = "".join(part + "\n" for part in text.split("\n")[:keep])
            self.truncated = True
        if self.max_chars is not None and self.chars + len(text) > self.max_chars:
            text = text[: max(0, self.max_chars - self.chars)]
            self.truncated = True
        self.chars += len(text)
        self.lines += text.count("\n")
        super().write(text)
        return size


def available(module: str) -> bool:
    return module in sys.modules or importlib.util.find_spec(module) is not None


def prelude_blocks(source: str, filename: str) -> list[tuple[str, object]]:
    """Делит prelude на блоки по импортам: [(пакет, код)] — настройки идут вместе с импортом своего пакета."""
    blocks: list[tuple[str, list[ast.stmt]]] = []
    for node in ast.parse(source, filename).body:
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            module = (node.names[0].name if isinstance(node, ast.Import) else node.module or "").split(".")[0]
            if not blocks or blocks[-1][0] != module:
                blocks.append((module, []))
        elif not blocks:
            raise ValueError(f"{filename}: до первого импорта не должно быть кода")
        blocks[-1][1].append(node)
    return [(module, compile(ast.Module(body, []), filename, "exec")) for module, body in blocks]


def is_plot_object(value) -> bool:
    """Оси, фигура или список линий matplotlib: вместо их repr статья показывает сам график."""
    items = list(value.flat) if type(value).__name__ == "ndarray" and value.dtype == object else value
    if isinstance(items, (list, tuple)):
        return bool(items) and all(is_plot_object(v) for v in items)
    return type(value).__module__.startswith("matplotlib.")


class ExampleRunner:
    """Выполняет ячейки в одинаковой обстановке: настройки отображения сбрасываются перед каждой."""

    def __init__(self, prelude_source: str, prelude_filename: str, max_chars: int | None = None, max_lines: int | None = None):
        os.environ["MPLBACKEND"] = "Agg"
        self.prelude = prelude_blocks(prelude_source, prelude_filename)
        self.max_chars, self.max_lines = max_chars, max_lines
        self.restore: dict[str, object] = {}  # пакет → функция, возвращающая его исходные настройки

    def capture_defaults(self):
        """Запоминает исходные настройки каждого доступного пакета — один раз, до первого выполнения prelude."""
        if "numpy" not in self.restore and available("numpy"):
            import numpy as np

            np_defaults = np.get_printoptions()
            self.restore["numpy"] = lambda: np.set_printoptions(**np_defaults)
        if "pandas" not in self.restore and available("pandas"):
            import pandas as pd
            from pandas._config.config import _registered_options

            pd_defaults = {k: pd.get_option(k) for k in _registered_options if k.startswith("display.")}

            def restore_pandas():
                for key, value in pd_defaults.items():
                    pd.set_option(key, value)

            self.restore["pandas"] = restore_pandas
        if "matplotlib" not in self.restore and available("matplotlib"):
            import matplotlib
            import matplotlib.pyplot as plt
            from cycler import cycler

            matplotlib.rcParams.update({**PLOT_RC, "axes.prop_cycle": cycler(color=PLOT_RC["axes.prop_cycle"])})
            mpl_defaults = {k: v for k, v in matplotlib.rcParams.items() if k != "backend"}

            def restore_matplotlib():
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")  # среди настроек matplotlib есть устаревшие
                    matplotlib.rcParams.update(mpl_defaults)
                plt.close("all")

            self.restore["matplotlib"] = restore_matplotlib

    def reset(self):
        self.capture_defaults()
        for restore in self.restore.values():
            restore()

    def run(self, setup: str, code: str, filename: str, cell_id: str) -> RunResult:
        self.reset()
        namespace: dict = {"__name__": "__main__"}
        buffer = LimitedOutput(self.max_chars, self.max_lines)
        categories: list[type] = []
        error: BaseException | None = None
        cell_file = f"{filename}:{cell_id}"
        packages = [module for module, _ in self.prelude if available(module)]

        def show(message, category, *_args, **_kwargs):
            categories.append(category)
            buffer.write(f"{category.__name__}: {message}\n")

        with warnings.catch_warnings(), tempfile.TemporaryDirectory() as workdir, contextlib.chdir(workdir):
            # у каждого примера своя пустая рабочая папка: можно писать и читать файлы
            warnings.simplefilter("always")
            warnings.showwarning = show
            with contextlib.redirect_stdout(buffer), contextlib.redirect_stderr(buffer):
                try:
                    for module, block in self.prelude:
                        if module in packages:
                            exec(block, namespace)
                    if setup:
                        exec(compile(setup, f"{filename}:setup", "exec"), namespace)
                    self.exec_cell(code, cell_file, namespace)
                except Exception as e:  # noqa: BLE001 — исключение и есть результат примера
                    error = e
            plt = sys.modules.get("matplotlib.pyplot")
            plots = [self.svg(plt.figure(n)) for n in plt.get_fignums()] if plt else []
            if plt:
                plt.close("all")
        truncated = buffer.truncated
        buffer.truncated, buffer.max_chars, buffer.max_lines = False, None, None  # текст ошибки виден всегда
        error_line = None
        if isinstance(error, SyntaxError) and error.filename == cell_file:
            error_line = error.lineno
            buffer.write(f"SyntaxError: {error.msg} (строка {error.lineno})\n")
        elif error is not None:
            tb = error.__traceback__
            while tb is not None:
                if tb.tb_frame.f_code.co_filename == cell_file:
                    error_line = tb.tb_lineno
                tb = tb.tb_next
            buffer.write(f"{type(error).__name__}: {error}\n")
        text = buffer.getvalue()
        lines = [l.rstrip() for l in text.rstrip("\n").split("\n")] if text else []
        return RunResult(lines, error, categories, plots, error_line, truncated, packages)

    @staticmethod
    def svg(figure) -> str:
        out = io.StringIO()
        figure.savefig(out, format="svg", metadata={"Date": None})  # без даты файл не меняется от запуска к запуску
        return out.getvalue()

    @staticmethod
    def exec_cell(code: str, filename: str, namespace: dict):
        tree = ast.parse(code, filename)
        last = tree.body[-1] if tree.body and isinstance(tree.body[-1], ast.Expr) else None
        if last is not None:
            tree.body.pop()
        exec(compile(tree, filename, "exec"), namespace)
        if last is not None:
            value = eval(compile(ast.Expression(last.value), filename, "eval"), namespace)
            if value is not None and not is_plot_object(value):
                print(repr(value))

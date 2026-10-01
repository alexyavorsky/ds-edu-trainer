"""Выполнение урока курса как ноутбука Jupyter — общее для валидатора (CPython) и сайта (Pyodide).

Этот модуль импортирует scripts/course_cpython.py, и он же выполняет ячейки урока в браузере
(runtime/pyodide_driver.py), поэтому сохранённый вывод и вывод на сайте получаются одним и тем же кодом.

- У урока одно пространство имён (LessonSession): переменные одной ячейки видны в следующих, как в Jupyter.
  Импорты в нём не подставляются — урок импортирует numpy и pandas сам, в первой ячейке.
- Перед началом сеанса courses/prelude.py задаёт настройки отображения (в отдельном пространстве имён —
  его импорты уроку не видны); настройки, изменённые прошлым сеансом, сбрасываются.
- Ячейка печатает stdout (и stderr), предупреждения — строкой «Категория: текст», затем repr последнего
  выражения (если не None). Таблица DataFrame дополнительно отдаётся в HTML — сайт показывает её как в Jupyter.
- У сеанса своя рабочая папка, в data/ — копии файлов данных урока: их можно менять, «Перезапустить»
  возвращает исходные.
- Проверка упражнения: код выполняется как обычная ячейка, затем тесты — функции test_* из раздела
  «проверка» — запускает тот же раннер, что у задач (runtime/runner.py). Тесты работают с копией пространства
  имён урока: свои функции и переменные они в урок не добавляют.
"""

from __future__ import annotations

import ast
import builtins
import contextlib
import os
import re
import shutil
import sys
import tempfile
import warnings
from dataclasses import dataclass, field
from pathlib import Path

from reference_exec import ExampleRunner, LimitedOutput, is_plot_object

RUNNER_SOURCE = Path(__file__).with_name("runner.py").read_text(encoding="utf-8")
_STYLE_RE = re.compile(r"<style[^>]*>.*?</style>\s*", re.S)


@dataclass
class CellResult:
    lines: list[str]  # stdout, stderr и предупреждения по порядку
    result: list[str] | None  # repr последнего выражения, по строкам
    html: str | None  # таблица DataFrame — вместо result на сайте
    error: BaseException | None
    error_text: str | None  # «Тип: сообщение»
    error_line: int | None  # строка ячейки, где возникло исключение
    categories: list[type] = field(default_factory=list)  # категории предупреждений
    plots: list[str] = field(default_factory=list)  # SVG открытых после ячейки фигур matplotlib
    truncated: bool = False

    def as_dict(self) -> dict:
        error = None
        if self.error is not None:
            error = {
                "type": type(self.error).__name__,
                "mro": [k.__name__ for k in type(self.error).__mro__],
                "text": self.error_text,
                "line": self.error_line,
            }
        return {
            "lines": self.lines,
            "result": self.result,
            "html": self.html,
            "error": error,
            "plots": self.plots,
            "warnings": sorted({c.__name__ for c in self.categories}),
            "truncated": self.truncated,
        }


def dataframe_html(value) -> str | None:
    """HTML таблицы DataFrame, как в Jupyter, но без встроенных стилей — оформление берёт сайт."""
    if type(value).__name__ != "DataFrame" or not type(value).__module__.startswith("pandas"):
        return None
    html = value._repr_html_()
    return _STYLE_RE.sub("", html).strip() if html else None


def test_names(source: str) -> list[str]:
    """Функции test_* верхнего уровня по порядку — как _TESTS у задач."""
    return [n.name for n in ast.parse(source).body if isinstance(n, ast.FunctionDef) and n.name.startswith("test_")]


class LessonSession:
    """Сеанс урока: пространство имён, рабочая папка с данными, настройки отображения."""

    def __init__(self, runner: ExampleRunner, data_dir: str | None, files: list[str], max_chars: int | None = None, max_lines: int | None = None):
        self.runner = runner
        self.max_chars, self.max_lines = max_chars, max_lines
        self.namespace: dict = {"__name__": "__main__", "__builtins__": builtins}
        self.workdir = tempfile.mkdtemp(prefix="lesson-")
        if files:
            os.makedirs(os.path.join(self.workdir, "data"))
            for name in files:
                shutil.copyfile(os.path.join(data_dir, name), os.path.join(self.workdir, "data", name))
        runner.reset()  # исходные настройки numpy/pandas/matplotlib: прошлый сеанс мог их поменять
        scratch: dict = {"__name__": "__prelude__"}
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            for module, block in runner.prelude:
                if module in sys.modules or _importable(module):
                    exec(block, scratch)

    def close(self) -> None:
        shutil.rmtree(self.workdir, ignore_errors=True)

    def run_cell(self, code: str, filename: str, scratch: bool = False) -> CellResult:
        """Выполняет ячейку в пространстве имён урока (scratch=True — в его копии: проверка ответа на вопрос)."""
        namespace = dict(self.namespace) if scratch else self.namespace
        buffer = LimitedOutput(self.max_chars, self.max_lines)
        categories: list[type] = []
        error: BaseException | None = None
        value = None

        def show(message, category, *_args, **_kwargs):
            categories.append(category)
            buffer.write(f"{category.__name__}: {message}\n")

        with warnings.catch_warnings(), contextlib.chdir(self.workdir):
            warnings.simplefilter("always")
            warnings.showwarning = show
            with contextlib.redirect_stdout(buffer), contextlib.redirect_stderr(buffer):
                try:
                    value = self.exec_cell(code, filename, namespace)
                except Exception as e:  # noqa: BLE001 — исключение показывается в выводе ячейки
                    error = e
            plt = sys.modules.get("matplotlib.pyplot")
            plots = [ExampleRunner.svg(plt.figure(n)) for n in plt.get_fignums()] if plt else []
            if plt:
                plt.close("all")

        truncated = buffer.truncated
        text = buffer.getvalue()
        lines = [l.rstrip() for l in text.rstrip("\n").split("\n")] if text else []
        result = html = None
        if error is None and value is not None and not is_plot_object(value):
            result_text = LimitedOutput(self.max_chars, self.max_lines)
            result_text.write(repr(value))
            truncated = truncated or result_text.truncated
            result = [l.rstrip() for l in result_text.getvalue().rstrip("\n").split("\n")]
            html = dataframe_html(value)
        error_text = error_line = None
        if isinstance(error, SyntaxError) and error.filename == filename:
            error_line = error.lineno
            error_text = f"SyntaxError: {error.msg} (строка {error.lineno})"
        elif error is not None:
            error_line = user_line(error, filename)
            error_text = f"{type(error).__name__}: {error}"
            if isinstance(error, MemoryError) or (isinstance(error, OverflowError) and "index-sized" in str(error)):
                error_text = f"{type(error).__name__}: не хватило памяти — возможно, создаётся слишком большой массив"
        return CellResult(lines, result, html, error, error_text, error_line, categories, plots, truncated)

    @staticmethod
    def exec_cell(code: str, filename: str, namespace: dict):
        """Как ячейка Jupyter: всё, кроме последнего выражения, выполняется; значение выражения возвращается."""
        tree = ast.parse(code, filename)
        last = tree.body[-1] if tree.body and isinstance(tree.body[-1], ast.Expr) else None
        if last is not None:
            tree.body.pop()
        exec(compile(tree, filename, "exec"), namespace)
        if last is not None:
            return eval(compile(ast.Expression(last.value), filename, "eval"), namespace)
        return None

    def check(self, code: str, tests: str, targets: list[str], filename: str, on_tests=None, on_start=None, on_result=None) -> dict:
        """Проверка упражнения: код ученика как ячейка, затем тесты на текущем состоянии урока.

        Возвращает {"cell": CellResult, "phase": "run" | "missing" | "tests", "results": [...]}:
        run — код ячейки упал (тесты не запускались), missing — переменная из заготовки не создана или ещё
        равна `...`, tests — результаты тестов (как у задач: passed · failed · error · not_written · timeout).
        """
        cell = self.run_cell(code, filename)
        if cell.error is not None:
            return {"cell": cell, "phase": "run", "results": []}
        for name in targets:
            if "." in name:  # «Класс.метод»: класс объявлен, метод дописан
                message = unfinished_method(code, self.namespace, *name.split(".", 1))
                if message is None:
                    continue
                return {"cell": cell, "phase": "missing", "results": [{"title": message, "status": "not_written", "message": "", "error_type": None, "line": None}]}
            value = self.namespace.get(name, _MISSING)
            if value is _MISSING:
                message = f"переменная {name} не создана — в решении должна быть строка «{name} = …»"
            elif value is Ellipsis:
                message = f"{name} пока равна ... — замените многоточие своим кодом"
            else:
                continue
            return {"cell": cell, "phase": "missing", "results": [{"title": message, "status": "not_written", "message": "", "error_type": None, "line": None}]}

        names = test_names(tests)
        namespace = dict(self.namespace)  # тесты видят состояние урока, но свои имена в него не добавляют
        namespace["__name__"] = "__edu_tests__"  # раннер в конце не запустит тесты сам
        footer = f"{tests}\n\n_TESTS = [{', '.join(names)}]\n\n{RUNNER_SOURCE}"
        with contextlib.chdir(self.workdir):
            exec(compile(footer, "проверка", "exec"), namespace)
            if on_tests:
                on_tests([namespace["_test_info"](fn) for fn in namespace["_TESTS"]])
            results = namespace["_run_tests"](verbose=False, on_start=on_start, on_result=on_result, user_file=filename)
        for r in results:
            r["message"] = plain_numbers(r["message"])
            m = re.fullmatch(r"NameError: name '(\w+)' is not defined", r["message"])
            if m and r["line"] is None:
                r["message"] = f"не найдена переменная {m[1]} — проверьте имя; если она из ячейки выше, выполните ячейки выше"
        return {"cell": cell, "phase": "tests", "results": results}


_MISSING = object()


def unfinished_method(code: str, namespace: dict, cls: str, method: str) -> str | None:
    """Класс из заготовки не объявлен или его метод всё ещё состоит из `...` — понятное сообщение вместо проваленных тестов."""
    if not isinstance(namespace.get(cls), type):
        return f"класс {cls} не объявлен — в решении должна быть строка «class {cls}…»"
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return None
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == cls:
            for item in node.body:
                if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)) and item.name == method:
                    body = item.body[1:] if item.body and isinstance(item.body[0], ast.Expr) and isinstance(item.body[0].value, ast.Constant) and isinstance(item.body[0].value.value, str) else item.body
                    if all(isinstance(b, ast.Expr) and isinstance(b.value, ast.Constant) and b.value.value is Ellipsis for b in body):
                        return f"метод {cls}.{method} пока состоит из ... — допишите его"
    return None
_NUMPY_REPR = re.compile(r"np\.(?:u?int|float)\d+\(([^()]*)\)|np\.str_\(('[^']*'|\"[^\"]*\")\)|np\.(True|False)_")


def plain_numbers(message: str) -> str:
    """«np.int64(66)» → «66»: в сообщениях проверок обёртки типов NumPy только мешают читать."""
    return _NUMPY_REPR.sub(lambda m: m.group(1) or m.group(2) or m.group(3), message)


def _importable(module: str) -> bool:
    import importlib.util

    return importlib.util.find_spec(module) is not None


def user_line(error: BaseException, filename: str) -> int | None:
    """Последняя строка ячейки в трассировке — там, где ошибка в коде ученика."""
    line = None
    tb = error.__traceback__
    while tb is not None:
        if tb.tb_frame.f_code.co_filename == filename:
            line = tb.tb_lineno
        tb = tb.tb_next
    return line

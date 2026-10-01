#!/usr/bin/env python3
"""CPython-часть проверки курсов: её запускает scripts/validate_courses.ts, задание — JSON на stdin, ответ — JSON в stdout.

    {"mode": "versions"}                          → версии Python, NumPy, pandas
    {"mode": "concepts", "snippets": {id: код}, "python": [[урок, …], …]}
                                                  → понятия в коде: {id: ["np.array", ".shape", "axis=", …]};
        уроки из "python" (курс о самом Python, по курсам и по порядку) — понятия ООП, см. python_concepts
    {"mode": "run", "runs": [{"files": [...], "steps": [...]}]}
        каждый прогон — новый сеанс урока (runtime/lesson_exec.py, как в браузере); шаг —
        {"op": "cell" | "quiz" | "check", "cell": id, "code": …, "tests": …, "targets": [...]} → результат шага
    {"mode": "notebook", "notebook": {...}}       → выполняет ячейки кода ноутбука по порядку в одном
        пространстве имён (как ядро Jupyter): вывод каждой ячейки и первая ошибка

Нужны NumPy и pandas версий из requirements-dev.txt (.venv).
"""

from __future__ import annotations

import ast
import builtins
import contextlib
import io
import json
import os
import re
import sys
import tempfile
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "runtime"))
os.environ.setdefault("MPLBACKEND", "Agg")

from lesson_exec import LessonSession  # noqa: E402 — тот же код, что выполняет уроки в браузере
from reference_exec import ExampleRunner  # noqa: E402

DATA = ROOT / "courses" / "data"
PRELUDE = ROOT / "courses" / "prelude.py"
MODULE_ALIASES = {"np", "pd", "plt"}


def versions() -> dict:
    import numpy
    import pandas

    return {"python": sys.version.split()[0], "numpy": numpy.__version__, "pandas": pandas.__version__}


# ─── Понятия ────────────────────────────────────────────────────────────────


def dotted(node: ast.AST) -> str | None:
    parts = []
    while isinstance(node, ast.Attribute):
        parts.append(node.attr)
        node = node.value
    if isinstance(node, ast.Name):
        parts.append(node.id)
        return ".".join(reversed(parts))
    return None


def concepts(code: str) -> list[str]:
    """np.x / pd.x — функции модулей (полным путём), .x — атрибуты и методы, x= — именованные аргументы, @ — матричное умножение.

    Имена новых столбцов в assign(имя=…) и в именованной агрегации agg(имя=(столбец, функция)) — не понятия."""
    tree = ast.parse(code)
    inner = {id(n.value) for n in ast.walk(tree) if isinstance(n, ast.Attribute)}
    # имена новых столбцов — не параметры: assign(revenue=…), agg(total=("price", "sum"))
    column_names = set()
    for n in ast.walk(tree):
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute):
            if n.func.attr == "assign":
                column_names.update(id(k) for k in n.keywords)
            elif n.func.attr in ("agg", "aggregate"):
                column_names.update(id(k) for k in n.keywords if isinstance(k.value, ast.Tuple))
    found: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Attribute) and id(node) not in inner:
            chain = dotted(node)
            if chain and chain.split(".")[0] in MODULE_ALIASES:
                found.add(chain)
                continue
            if not node.attr.startswith("__"):
                found.add(f".{node.attr}")
            # методы в цепочке: orders.columns.tolist() → .columns и .tolist
            value = node.value
            while isinstance(value, ast.Attribute):
                found.add(f".{value.attr}")
                value = value.value
        elif isinstance(node, ast.keyword) and node.arg and id(node) not in column_names:
            found.add(f"{node.arg}=")
        elif isinstance(node, (ast.BinOp, ast.AugAssign)) and isinstance(node.op, ast.MatMult):
            found.add("@")
    return sorted(found)


# ─── Понятия курса о самом Python (ООП) ─────────────────────────────────────

# встроенные функции, которые курс объясняет (остальные — Python-минимум, известны с начала)
PYTHON_CALLS = {"type", "isinstance", "issubclass", "hasattr", "getattr", "setattr", "super", "repr", "hash", "iter", "next", "vars", "callable"}
MANGLED = re.compile(r"_[A-Za-z]\w*__\w+")


def declared_names(code: str) -> set[str]:
    """Имена, которые урок объявляет сам: атрибуты (self.x = …, атрибуты и поля класса), методы, параметры функций."""
    names: set[str] = set()
    for node in ast.walk(ast.parse(code)):
        if isinstance(node, ast.ClassDef):
            names.add(node.name)
            for item in node.body:
                if isinstance(item, ast.Assign):
                    names.update(t.id for t in item.targets if isinstance(t, ast.Name))
                elif isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
                    names.add(item.target.id)
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            names.add(node.name)
            a = node.args
            names.update(x.arg for x in [*a.posonlyargs, *a.args, *a.kwonlyargs])
        elif isinstance(node, (ast.Assign, ast.AugAssign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            for t in targets:
                for sub in ast.walk(t):
                    if isinstance(sub, ast.Attribute):
                        names.add(sub.attr)
    return names


def python_concepts(code: str, declared: set[str]) -> list[str]:
    """Понятия ООП: конструкции (class, class(Base), магические методы, декораторы, super(), raise, yield, is),
    импорты «модуль.имя», встроенные функции из PYTHON_CALLS, .x — только чужие атрибуты (не объявленные уроком),
    x= — только у чужих вызовов. Магические атрибуты (.__dict__, .__name__) — тоже понятия."""
    tree = ast.parse(code)
    found: set[str] = set()
    # @price.setter — понятие «@setter», а не атрибут .setter
    in_decorators = {id(d.func if isinstance(d, ast.Call) else d) for n in ast.walk(tree) if isinstance(n, (ast.ClassDef, ast.FunctionDef)) for d in n.decorator_list}
    for node in ast.walk(tree):
        if id(node) in in_decorators and isinstance(node, ast.Attribute):
            continue
        if isinstance(node, ast.ClassDef):
            found.add("class(Base)" if node.bases else "class")
            for dec in node.decorator_list:
                found.add(decorator_name(dec))
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.name.startswith("__") and node.name.endswith("__"):
                found.add(node.name)
            for dec in node.decorator_list:
                found.add(decorator_name(dec))
        elif isinstance(node, ast.Raise):
            found.add("raise from" if node.cause is not None else "raise")
        elif isinstance(node, (ast.Yield, ast.YieldFrom)):
            found.add("yield")
        elif isinstance(node, ast.Compare) and any(isinstance(op, (ast.Is, ast.IsNot)) for op in node.ops):
            found.add("is")
        elif isinstance(node, ast.ImportFrom) and node.module:
            found.update(f"{node.module}.{a.name}" for a in node.names)
        elif isinstance(node, ast.Import):
            found.update(f"import {a.name}" for a in node.names)
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in PYTHON_CALLS:
            found.add(f"{node.func.id}()" if node.func.id == "super" else node.func.id)
        elif isinstance(node, ast.Attribute):
            attr = node.attr
            if attr.startswith("__") and attr.endswith("__"):
                if attr not in declared:
                    found.add(f".{attr}")
            elif attr not in declared and not MANGLED.fullmatch(attr):
                found.add(f".{attr}")
        elif isinstance(node, ast.keyword) and node.arg and node.arg not in declared:
            found.add(f"{node.arg}=")
    found.discard("")
    return sorted(found)


def decorator_name(dec: ast.AST) -> str:
    """@property → «@property», @price.setter → «@setter»; импортированные (@dataclass) — понятие своего импорта."""
    target = dec.func if isinstance(dec, ast.Call) else dec
    if isinstance(target, ast.Attribute):
        return f"@{target.attr}"
    return f"@{target.id}" if isinstance(target, ast.Name) and target.id in {"property", "classmethod", "staticmethod"} else ""


def concepts_task(snippets: dict[str, str], python_courses: list[list[str]]) -> dict:
    result: dict = {}
    python_lessons = {lesson for course in python_courses for lesson in course}
    for key, code in snippets.items():
        if key.split("#")[0] in python_lessons:
            continue
        try:
            result[key] = concepts(code)
        except SyntaxError as e:
            result[key] = {"error": f"SyntaxError: {e.msg} (строка {e.lineno})"}
    for course in python_courses:
        declared: set[str] = set()
        for lesson in course:
            own = {k: v for k, v in snippets.items() if k.split("#")[0] == lesson}
            for code in own.values():
                with contextlib.suppress(SyntaxError):
                    declared |= declared_names(code)
            for key, code in own.items():
                try:
                    result[key] = python_concepts(code, declared)
                except SyntaxError as e:
                    result[key] = {"error": f"SyntaxError: {e.msg} (строка {e.lineno})"}
    return result


# ─── Прогоны урока ──────────────────────────────────────────────────────────


def run_lessons(runs: list[dict]) -> list[list[dict]]:
    runner = ExampleRunner(PRELUDE.read_text(encoding="utf-8"), str(PRELUDE))
    out = []
    for run in runs:
        session = LessonSession(runner, str(DATA), run["files"])
        steps = []
        try:
            for step in run["steps"]:
                filename = f"{run['lesson']}:{step['cell']}"
                if step["op"] == "check":
                    outcome = session.check(step["code"], step["tests"], step["targets"], filename)
                    steps.append({**outcome["cell"].as_dict(), "phase": outcome["phase"], "results": outcome["results"]})
                else:
                    steps.append(session.run_cell(step["code"], filename, scratch=step["op"] == "quiz").as_dict())
        finally:
            session.close()
        out.append(steps)
    return out


# ─── Ноутбук ────────────────────────────────────────────────────────────────


def run_notebook(notebook: dict) -> dict:
    """Ячейки кода по порядку в одном пространстве имён, как ядро Jupyter; stdout каждой — для сверки итогов."""
    namespace: dict = {"__name__": "__main__", "__builtins__": builtins}
    outputs = []
    with tempfile.TemporaryDirectory() as workdir, contextlib.chdir(workdir):
        for cell in notebook["cells"]:
            if cell["cell_type"] != "code":
                continue
            source = "".join(cell["source"])
            buffer = io.StringIO()
            try:
                with contextlib.redirect_stdout(buffer), contextlib.redirect_stderr(buffer):
                    exec(compile(source, f"ячейка {cell['id']}", "exec"), namespace)
            except Exception:  # noqa: BLE001 — ошибка ячейки и есть результат проверки
                return {"outputs": outputs, "error": {"cell": cell["id"], "traceback": traceback.format_exc(limit=3)}}
            finally:
                plt = sys.modules.get("matplotlib.pyplot")
                if plt is not None:
                    plt.close("all")  # как inline-бэкенд Jupyter: фигура ячейки показана и закрыта, следующая ячейка рисует новую
            outputs.append({"cell": cell["id"], "stdout": buffer.getvalue()})
    return {"outputs": outputs, "error": None}


def main() -> None:
    task = json.load(sys.stdin)
    out = sys.stdout
    sys.stdout = sys.stderr  # всё, что уроки печатают мимо перехвата (например, из тестов), — не в ответ JSON
    mode = task["mode"]
    if mode == "versions":
        result = versions()
    elif mode == "concepts":
        result = concepts_task(task["snippets"], task.get("python", []))
    elif mode == "run":
        result = run_lessons(task["runs"])
    elif mode == "notebook":
        result = run_notebook(task["notebook"])
    else:
        raise SystemExit(f"неизвестный режим {mode}")
    out.write(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""CPython-часть проверки курсов: её запускает scripts/validate_courses.ts, задание — JSON на stdin, ответ — JSON в stdout.

    {"mode": "versions"}                          → версии Python, NumPy, pandas
    {"mode": "concepts", "snippets": {id: код}}   → понятия в коде: {id: ["np.array", ".shape", "axis=", …]}
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
    """Версии Python и пакетов курсов; нет пакета — None (курсу без пакета, например ООП, он не нужен)."""
    import importlib.metadata as md

    found: dict = {"python": sys.version.split()[0]}
    for name in ("numpy", "pandas"):
        try:
            found[name] = md.version(name)
        except md.PackageNotFoundError:
            found[name] = None
    return found


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


PY_CALLS = {"super", "isinstance", "issubclass", "hasattr", "getattr", "setattr"}  # понятия-вызовы курса по языку


def declared_names(code: str) -> set[str]:
    """Имена, которые код объявляет сам: классы, функции, методы, атрибуты self.x и класса, поля dataclass.

    Для курса по языку (ООП): обращение .x к своему атрибуту и x= в вызове своего класса — не новые понятия."""
    names: set[str] = set()
    for node in ast.walk(ast.parse(code)):
        if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            names.add(node.name)
            if not isinstance(node, ast.ClassDef):
                names.update(a.arg for a in [*node.args.posonlyargs, *node.args.args, *node.args.kwonlyargs])
            else:
                for item in node.body:
                    if isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
                        names.add(item.target.id)
                    elif isinstance(item, ast.Assign):
                        names.update(t.id for t in item.targets if isinstance(t, ast.Name))
        elif isinstance(node, ast.Attribute) and isinstance(node.ctx, ast.Store):
            names.add(node.attr)
    return names


def python_concepts(tree: ast.Module, declared: set[str]) -> set[str]:
    """Конструкции языка как понятия (курс ООП): class, наследование, магические методы, декораторы, super() …"""
    found: set[str] = set()
    called = {id(n.func) for n in ast.walk(tree) if isinstance(n, ast.Call)}
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            found.add("class(Base)" if node.bases else "class")
            for item in node.body:
                if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)) and item.name.startswith("__") and item.name.endswith("__"):
                    found.add(f"def {item.name}")
        if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            for d in node.decorator_list:
                target = d.func if isinstance(d, ast.Call) else d
                name = target.attr if isinstance(target, ast.Attribute) else target.id if isinstance(target, ast.Name) else None
                if name and name not in declared - {"setter", "getter", "deleter"}:
                    found.add(f"@{name}")
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in PY_CALLS:
            found.add(f"{node.func.id}()")
        elif isinstance(node, ast.Raise):
            found.add("raise from" if node.cause is not None else "raise")
        elif isinstance(node, (ast.Yield, ast.YieldFrom)):
            found.add("yield")
        elif isinstance(node, ast.Import):
            found.update(f"import {a.name.split('.')[0]}" for a in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module and not node.level:
            found.add(f"import {node.module.split('.')[0]}")
        elif isinstance(node, ast.Attribute) and node.attr.startswith("__") and node.attr.endswith("__") and id(node) not in called:
            found.add(f".{node.attr}")  # магические атрибуты: __dict__, __mro__, __class__ (вызов super().__init__() — нет)
    return found


def concepts(code: str, python_mode: bool = False, declared: set[str] | frozenset[str] = frozenset()) -> list[str]:
    """np.x / pd.x — функции модулей (полным путём), .x — атрибуты и методы, x= — именованные аргументы, @ — матричное умножение.

    Имена новых столбцов в assign(имя=…) и в именованной агрегации agg(имя=(столбец, функция)) — не понятия.
    python_mode (курс по языку, concepts = "python" в course.toml): .x и x= не считаются, если x объявлен в коде
    урока или прошлых уроков (declared) или вызывается свой класс / функция; плюс конструкции — python_concepts."""
    tree = ast.parse(code)
    inner = {id(n.value) for n in ast.walk(tree) if isinstance(n, ast.Attribute)}
    own_calls = set()  # именованные аргументы вызовов своих классов и функций — не понятия
    if python_mode:
        for n in ast.walk(tree):
            if isinstance(n, ast.Call):
                callee = n.func.attr if isinstance(n.func, ast.Attribute) else n.func.id if isinstance(n.func, ast.Name) else None
                if callee in declared:
                    own_calls.update(id(k) for k in n.keywords)
            if isinstance(n, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):  # @x.setter — понятие «@setter», не «.setter»
                inner.update(id(d.func if isinstance(d, ast.Call) else d) for d in n.decorator_list)
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
            if not node.attr.startswith("__") and node.attr not in declared:
                found.add(f".{node.attr}")
            # методы в цепочке: orders.columns.tolist() → .columns и .tolist
            value = node.value
            while isinstance(value, ast.Attribute):
                if value.attr not in declared:
                    found.add(f".{value.attr}")
                value = value.value
        elif isinstance(node, ast.keyword) and node.arg and id(node) not in column_names and id(node) not in own_calls:
            found.add(f"{node.arg}=")
        elif isinstance(node, (ast.BinOp, ast.AugAssign)) and isinstance(node.op, ast.MatMult):
            found.add("@")
    if python_mode:
        found |= python_concepts(tree, set(declared))
    return sorted(found)


def collect_concepts(snippets: dict[str, str], python_lessons: list[list[str]]) -> dict:
    """Понятия каждого фрагмента. python_lessons — уроки курсов по языку по порядку: имена, объявленные в уроке и
    в прошлых уроках курса, накапливаются и не считаются понятиями."""
    result: dict = {}
    mode: dict[str, set[str]] = {}  # урок → объявленные имена (только у курсов по языку)
    for lessons in python_lessons:
        declared: set[str] = set()
        for lesson in lessons:
            for key, code in snippets.items():
                if key.startswith(f"{lesson}#"):
                    with contextlib.suppress(SyntaxError):
                        declared |= declared_names(code)
            mode[lesson] = set(declared)
    for key, code in snippets.items():
        lesson = key.split("#")[0]
        try:
            result[key] = concepts(code, lesson in mode, mode.get(lesson, set()))
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
        result = collect_concepts(task["snippets"], task.get("python", []))
    elif mode == "run":
        result = run_lessons(task["runs"])
    elif mode == "notebook":
        result = run_notebook(task["notebook"])
    else:
        raise SystemExit(f"неизвестный режим {mode}")
    out.write(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()

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
    """np.x / pd.x — функции модулей (полным путём), .x — атрибуты и методы, x= — именованные аргументы."""
    tree = ast.parse(code)
    inner = {id(n.value) for n in ast.walk(tree) if isinstance(n, ast.Attribute)}
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
        elif isinstance(node, ast.keyword) and node.arg:
            found.add(f"{node.arg}=")
    return sorted(found)


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
        result = {}
        for key, code in task["snippets"].items():
            try:
                result[key] = concepts(code)
            except SyntaxError as e:
                result[key] = {"error": f"SyntaxError: {e.msg} (строка {e.lineno})"}
    elif mode == "run":
        result = run_lessons(task["runs"])
    elif mode == "notebook":
        result = run_notebook(task["notebook"])
    else:
        raise SystemExit(f"неизвестный режим {mode}")
    out.write(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()

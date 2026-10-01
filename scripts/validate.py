#!/usr/bin/env python3
"""Валидация задач в challenges/.

Для каждой задачи проверяет:
  1. meta.toml: все обязательные поля на месте и корректны;
  2. набор файлов соответствует типу задачи, .py компилируются;
  3. собранный файл с solution.py проходит все тесты;
  4. собранный файл со starter.py НЕ проходит хотя бы один тест.

Собирается ровно тот .py, который сайт показывает в копируемом блоке
(та же склейка: docstring + код + tests.py + runtime/runner.py).

Использование:
  python3 scripts/validate.py                      # все задачи
  python3 scripts/validate.py --chapter 03-recursion
  python3 scripts/validate.py --bundle <папка-задачи> [--solution]   # напечатать сборку

Требуется Python 3.11+ (tomllib). Только стандартная библиотека.
"""

from __future__ import annotations

import argparse
import ast
import difflib
import json
import os
import re
import subprocess
import sys
import tempfile
import textwrap
import tomllib
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# EDU_CONTENT_ROOT — другая папка с той же структурой (образцы платформы tests/platform), как в src/lib/paths.ts
CONTENT = (ROOT / os.environ["EDU_CONTENT_ROOT"]).resolve() if os.environ.get("EDU_CONTENT_ROOT") else ROOT
CHALLENGES = CONTENT / "challenges"
RUNNER = ROOT / "runtime" / "runner.py"
REQUIREMENTS = ROOT / "requirements-dev.txt"

DIFFICULTIES = ("easy", "medium", "hard")
TYPES = ("implement", "fix-bug", "complete", "complexity")
DIFFICULTY_RU = {"easy": "лёгкая", "medium": "средняя", "hard": "сложная"}
TYPE_RU = {
    "implement": "реализовать",
    "fix-bug": "найти ошибку",
    "complete": "дописать",
    "complexity": "оценить сложность",
}

CODE_FILES = ("task.md", "starter.py", "solution.py", "tests.py")
COMPLEXITY_FILES = ("task.md", "code.py")
IGNORED_FILES = {"__pycache__", ".DS_Store"}
DATA_FILE = "data.py"  # необязательные данные задачи: в копируемом файле — блок перед заготовкой, тесты их используют
DATA_MAX_LINES = 150
MUTANTS_FILE = "mutants.toml"  # типичные ошибки: «найти → заменить» в solution.py; каждая должна ловиться тестами
ALT_DIR = "alt_solutions"  # корректные, но «неэкономные» решения: должны проходить тесты, на сайте не показываются

META_REQUIRED = {"id", "title", "difficulty", "type", "tags", "hints"}
META_OPTIONAL = {"bugs", "order", "refs", "lessons", "complexity"}
# book.toml описывает раздел задач: книгу (kind = "book") или тему (kind = "topic", например NumPy).
BOOK_REQUIRED = {"title", "code", "direction"}
BOOK_OPTIONAL = {"kind", "author", "edition", "order", "description", "packages", "reference", "beta"}
# Направления сайта (группы на главной и в меню) — как DIRECTIONS в src/lib/directions.ts.
DIRECTIONS = ("python", "data", "git", "english")
BOOK_KINDS = ("book", "topic")
# Задачи по книгам — только стандартная библиотека; у темы разрешены пакеты из её поля packages.
KNOWN_PACKAGES = {"numpy", "pandas"}
CHAPTER_REQUIRED = {"title", "summary"}
CHAPTER_OPTIONAL = {"book_chapter"}

SLUG_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
CHAPTER_DIR_RE = re.compile(r"^(\d{2})-[a-z0-9]+(-[a-z0-9]+)*$")
RESULT_MARK = "@@RESULTS@@"
TIMEOUT = 15
PYTHON_MIN = (3, 10)  # задачи должны запускаться на Python 3.10+
MIN_TESTS = 3
SEPARATOR = "# ════ Тесты — ниже этой линии ничего менять не нужно " + "═" * 19
DATA_SEPARATOR = "# ════ Данные задачи — их можно вызывать в своём коде " + "═" * 19
CODE_SEPARATOR = "# ════ Решение " + "═" * 58
TESTS_LIST_COMMENT = "# Тесты задачи по порядку — запускаются только они"


# ─── Сборка копируемого файла ───────────────────────────────────────────────


DOCSTRING_SECTIONS = ("Ограничения", "Правила")  # нормативные разделы task.md, которые попадают в docstring


def strip_emphasis(text: str) -> str:
    """Убирает **жирный** и *курсив* вне `кода`."""
    parts = text.split("`")
    for i in range(0, len(parts), 2):
        parts[i] = re.sub(r"\*\*(.+?)\*\*", r"\1", parts[i])
        parts[i] = re.sub(r"\*(\S(?:.*?\S)?)\*", r"\1", parts[i])
    return "`".join(parts)


def first_paragraph(markdown: str) -> str:
    lines: list[str] = []
    for line in markdown.strip().splitlines():
        if not line.strip():
            if lines:
                break
            continue
        lines.append(line.strip())
    return strip_emphasis(" ".join(lines))


def docstring_sections(markdown: str) -> list[tuple[str, list[tuple[str, str]]]]:
    """Разделы «Ограничения»/«Правила»: [(заголовок, [(маркер пункта или "", текст), …])]."""
    result: list[tuple[str, list[list]]] = []
    items: list[list] | None = None
    new_paragraph = True
    for line in markdown.splitlines():
        if line.startswith("## "):
            title = line[3:].strip()
            items = [] if title in DOCSTRING_SECTIONS else None
            if items is not None:
                result.append((title, items))
            new_paragraph = True
            continue
        if items is None:
            continue
        stripped = line.strip()
        if not stripped:
            new_paragraph = True
        elif marker := re.match(r"(- |\d+\. )", stripped):
            items.append([marker.group(1), stripped[marker.end():].strip()])
            new_paragraph = False
        elif items and not new_paragraph:
            items[-1][1] += " " + stripped
        else:
            items.append(["", stripped])
            new_paragraph = False
    return [(title, [(marker, strip_emphasis(text)) for marker, text in its]) for title, its in result if its]


def fill(text: str, initial: str = "", subsequent: str = "") -> str:
    # перенос только по пробелам — так же, как в src/lib/bundle.ts
    return textwrap.fill(
        text, width=76, initial_indent=initial, subsequent_indent=subsequent, break_on_hyphens=False, break_long_words=False
    )


def chapter_label(chapter_dir: Path, chapter_meta: dict, kind: str = "book") -> str:
    number = int(chapter_dir.name[:2])
    word = "Раздел" if kind == "topic" else "Глава"  # у темы главы повторяют разделы справочника
    return f"{word} {number}. {chapter_meta['title']}"


def pinned_versions() -> dict[str, str]:
    """Версии из requirements-dev.txt: на них проверены задачи тем (строка «Нужно: …» в docstring)."""
    pins = {}
    for line in REQUIREMENTS.read_text("utf-8").splitlines() if REQUIREMENTS.exists() else []:
        m = re.match(r"^([A-Za-z0-9_.-]+)==([^\s#]+)", line)
        if m:
            pins[m[1].lower()] = m[2]
    return pins


def needs_line(packages: list[str], pins: dict[str, str]) -> str:
    """«Нужно: numpy (проверено на 2.5.3)» — зеркало src/lib/bundle.ts::needsLine."""
    return "Нужно: " + ", ".join(f"{p} (проверено на {pins[p]})" if p in pins else p for p in packages)


def build_bundle(task_dir: Path, code_file: str = "starter.py", code: str | None = None) -> str:
    """Склеивает запускаемый .py. Логика зеркалится в src/lib/bundle.ts."""
    chapter_dir, book_dir = task_dir.parent, task_dir.parent.parent
    meta = load_toml(task_dir / "meta.toml")
    chapter_meta = load_toml(chapter_dir / "chapter.toml")
    book_meta = load_toml(book_dir / "book.toml")

    task_md = (task_dir / "task.md").read_text("utf-8")
    extra: list[str] = []
    for title, items in docstring_sections(task_md):
        extra += [f"{title}:"] + [fill(text, marker, " " * len(marker)) for marker, text in items] + [""]
    header = "\n".join(
        [
            '"""',
            meta["title"],
            f"{book_meta['title']} → {chapter_label(chapter_dir, chapter_meta, book_meta.get('kind', 'book'))}",
            f"Сложность: {DIFFICULTY_RU[meta['difficulty']]} · Тип: {TYPE_RU[meta['type']]} · id: {meta['id']}",
            "",
            fill(first_paragraph(task_md)),
            "",
            *extra,
            *([needs_line(book_meta["packages"], pinned_versions())] if book_meta.get("packages") else []),
            f"Запуск: python3 {task_dir.name.replace('-', '_')}.py (на Windows: python {task_dir.name.replace('-', '_')}.py)",
            '"""',
        ]
    )
    code = (code if code is not None else (task_dir / code_file).read_text("utf-8")).strip()
    tests = (task_dir / "tests.py").read_text("utf-8").strip()
    runner = RUNNER.read_text("utf-8").strip()
    data_path = task_dir / DATA_FILE
    if data_path.exists():  # данные — перед заготовкой: их можно вызвать в своём коде и посмотреть
        header += f"\n\n{DATA_SEPARATOR}\n\n{data_path.read_text('utf-8').strip()}\n\n\n{CODE_SEPARATOR}"
    return f"{header}\n\n{code}\n\n\n{SEPARATOR}\n\n{tests}\n\n\n{tests_list(tests)}\n\n\n{runner}\n"


def tests_list(tests: str) -> str:
    """Явный список тестов после tests.py: функция test_… из кода решения тестом не становится.

    Имена — функции test_* верхнего уровня tests.py по порядку (зеркало src/lib/bundle.ts::testsList).
    """
    names = [n.name for n in ast.parse(tests).body if isinstance(n, ast.FunctionDef) and n.name.startswith("test_")]
    return "\n".join([TESTS_LIST_COMMENT, "_TESTS = [", *(f"    {name}," for name in names), "]"])


# ─── Отчёт ──────────────────────────────────────────────────────────────────


@dataclass
class TaskReport:
    path: Path
    meta: dict = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    solution_result: str = ""
    starter_result: str = ""
    alt_result: str = ""
    mutant_result: str = ""

    @property
    def ok(self) -> bool:
        return not self.errors


def load_toml(path: Path) -> dict:
    with path.open("rb") as f:
        return tomllib.load(f)


def check_keys(data: dict, required: set[str], optional: set[str], where: str, errors: list[str]) -> None:
    missing = required - data.keys()
    unknown = data.keys() - required - optional
    if missing:
        errors.append(f"{where}: нет обязательных полей: {', '.join(sorted(missing))}")
    if unknown:
        errors.append(f"{where}: неизвестные поля (опечатка?): {', '.join(sorted(unknown))}")


def is_str_list(value: object, allow_empty: bool = True) -> bool:
    return (
        isinstance(value, list)
        and (allow_empty or bool(value))
        and all(isinstance(v, str) and v.strip() for v in value)
    )


# ─── Проверка meta.toml ─────────────────────────────────────────────────────


def check_meta(r: TaskReport, book_code: str) -> None:
    try:
        meta = load_toml(r.path / "meta.toml")
    except FileNotFoundError:
        r.errors.append("нет meta.toml")
        return
    except tomllib.TOMLDecodeError as e:
        r.errors.append(f"meta.toml не парсится: {e}")
        return
    r.meta = meta
    check_keys(meta, META_REQUIRED, META_OPTIONAL, "meta.toml", r.errors)

    task_id = meta.get("id")
    if not isinstance(task_id, str) or not SLUG_RE.match(task_id):
        r.errors.append(f"id должен быть в kebab-case, получено {task_id!r}")
    elif not task_id.startswith(f"{book_code}-"):
        r.errors.append(f"id должен начинаться с префикса книги «{book_code}-»: {task_id}")

    if not isinstance(meta.get("title"), str) or not meta.get("title", "").strip():
        r.errors.append("title пустой")
    if meta.get("difficulty") not in DIFFICULTIES:
        r.errors.append(f"difficulty должен быть одним из {DIFFICULTIES}, получено {meta.get('difficulty')!r}")
    if meta.get("type") not in TYPES:
        r.errors.append(f"type должен быть одним из {TYPES}, получено {meta.get('type')!r}")
    if not is_str_list(meta.get("tags"), allow_empty=False):
        r.errors.append("tags: нужен непустой список строк")
    if not is_str_list(meta.get("hints")):
        r.errors.append("hints: нужен список непустых строк (может быть пустым)")
    if "order" in meta and not isinstance(meta["order"], int):
        r.errors.append("order должен быть целым числом")
    if "refs" in meta and not is_str_list(meta["refs"]):
        r.errors.append("refs: нужен список строк вида «тема/статья»")
    elif "refs" in meta:
        known = reference_articles()
        for ref in meta["refs"]:
            if ref not in known:
                r.errors.append(f"refs: статьи справочника «{ref}» нет (ожидается «тема/статья», например numpy/broadcasting)")
    if "lessons" in meta and not is_str_list(meta["lessons"]):
        r.errors.append("lessons: нужен список id уроков курсов, например [\"np-broadcasting\"]")
    elif "lessons" in meta:
        known_lessons = course_lessons()
        for lesson in meta["lessons"]:
            if lesson not in known_lessons:
                r.errors.append(f"lessons: урока «{lesson}» нет в courses/ (нужен id из frontmatter lesson.mdx, например np-first-array)")

    task_type = meta.get("type")
    if task_type == "fix-bug":
        bugs = meta.get("bugs")
        if not isinstance(bugs, int) or not 1 <= bugs <= 3:
            r.errors.append("fix-bug: поле bugs обязательно, целое от 1 до 3")
    elif "bugs" in meta:
        r.errors.append("bugs допустимо только для type = fix-bug")

    if task_type == "complexity":
        c = meta.get("complexity")
        if not isinstance(c, dict):
            r.errors.append("complexity: нужна таблица [complexity] с options / answer / explanation")
        else:
            check_keys(c, {"options", "answer", "explanation"}, set(), "[complexity]", r.errors)
            options = c.get("options")
            if not is_str_list(options) or not 3 <= len(options) <= 5:
                r.errors.append("[complexity].options: от 3 до 5 непустых строк")
            elif len(set(options)) != len(options):
                r.errors.append("[complexity].options: варианты повторяются")
            elif c.get("answer") not in options:
                r.errors.append(f"[complexity].answer {c.get('answer')!r} нет среди options")
            if not isinstance(c.get("explanation"), str) or not c.get("explanation", "").strip():
                r.errors.append("[complexity].explanation пустой")
    elif "complexity" in meta:
        r.errors.append("[complexity] допустима только для type = complexity")


# ─── Проверка файлов и кода ─────────────────────────────────────────────────


def check_files(r: TaskReport) -> bool:
    expected = COMPLEXITY_FILES if r.meta.get("type") == "complexity" else CODE_FILES
    present = {p.name for p in r.path.iterdir()} - IGNORED_FILES
    missing = [f for f in expected if f not in present]
    for f in missing:
        r.errors.append(f"нет файла {f}")
    extra = present - set(expected) - {"meta.toml", ALT_DIR, MUTANTS_FILE, *((DATA_FILE,) if r.meta.get("type") != "complexity" else ())}
    if extra:
        r.warnings.append(f"лишние файлы: {', '.join(sorted(extra))}")
    return not missing


def check_task_md(r: TaskReport) -> None:
    text = (r.path / "task.md").read_text("utf-8")
    para = first_paragraph(text)
    if not para or para.startswith("#"):
        r.errors.append("task.md: первый абзац должен быть кратким условием (не заголовком)")
    doc_text = para + " ".join(t for _, items in docstring_sections(text) for _, t in items)
    if '"""' in doc_text or "\\" in doc_text:
        r.errors.append('task.md: в первом абзаце и разделах «Ограничения»/«Правила» нельзя использовать """ и \\ (они уходят в docstring)')
    if len(para) > 500:
        r.warnings.append(f"task.md: первый абзац длинный ({len(para)} симв.) — docstring будет громоздким")


def parse_py(r: TaskReport, name: str) -> ast.Module | None:
    """Разбирает файл; синтаксис должен быть совместим с Python 3.10."""
    try:
        return ast.parse((r.path / name).read_text("utf-8"), filename=name, feature_version=PYTHON_MIN)
    except SyntaxError as e:
        r.errors.append(f"{name}: синтаксическая ошибка (или синтаксис новее Python 3.10): {e}")
        return None


def function_signature(node: ast.FunctionDef | ast.AsyncFunctionDef, with_decorators: bool = True) -> str:
    """У методов декораторы — часть интерфейса (@property, @classmethod); у функций — нет (@cache в решении — можно)."""
    decorators = "".join(f"@{ast.unparse(d)} " for d in node.decorator_list) if with_decorators else ""
    returns = f" -> {ast.unparse(node.returns)}" if node.returns else ""
    return f"{decorators}({ast.unparse(node.args)}){returns}"


def is_public(name: str) -> bool:
    """Публичный интерфейс класса: обычные имена и магические методы (__init__, __eq__…), но не _внутренние."""
    return not name.startswith("_") or (name.startswith("__") and name.endswith("__"))


def class_signature(node: ast.ClassDef) -> str:
    """Декораторы и базовые классы: «@dataclass(frozen=True) class(Base)»."""
    decorators = "".join(f"@{ast.unparse(d)} " for d in node.decorator_list)
    bases = ", ".join(ast.unparse(b) for b in [*node.bases, *node.keywords])
    return f"{decorators}class({bases})"


def signatures(tree: ast.Module) -> dict[str, str]:
    """Имя → сигнатура: функции верхнего уровня, классы (декораторы и базы) и их публичные методы «Класс.метод»."""
    result = {}
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            result[node.name] = function_signature(node, with_decorators=False)
        elif isinstance(node, ast.ClassDef):
            result[node.name] = class_signature(node)
            for item in node.body:
                if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)) and is_public(item.name):
                    key = f"{node.name}.{item.name}"
                    # свойство с сеттером: два метода с одним именем — сигнатуры через «|»
                    result[key] = f"{result[key]} | {function_signature(item)}" if key in result else function_signature(item)
    return result


def class_members(tree: ast.Module) -> set[str]:
    """Публичные методы и атрибуты уровня класса (поля dataclass) — для проверки, что видит tests.py.

    Атрибуты экземпляра (self.x = …) не учитываются: в заготовке implement тело __init__ — raise NotImplementedError."""
    names: set[str] = set()
    for cls in (n for n in tree.body if isinstance(n, ast.ClassDef)):
        for node in cls.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                names.add(node.name)
            elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
                names.add(node.target.id)
            elif isinstance(node, ast.Assign):
                names.update(t.id for t in node.targets if isinstance(t, ast.Name))
    return {n for n in names if is_public(n)}


def check_code(r: TaskReport) -> bool:
    starter = parse_py(r, "starter.py")
    solution = parse_py(r, "solution.py")
    tests = parse_py(r, "tests.py")
    if not (starter and solution and tests):
        return False

    s_sig, sol_sig = signatures(starter), signatures(solution)
    for name, sig in s_sig.items():
        if name not in sol_sig:
            r.errors.append(f"в solution.py нет {name}, объявленного в starter.py")
        elif sol_sig[name] != sig:
            r.errors.append(f"сигнатура {name} различается: starter {sig} ≠ solution {sol_sig[name]}")
    starter_classes = {n.name for n in starter.body if isinstance(n, ast.ClassDef)}
    for name in sorted(sol_sig.keys() - s_sig.keys()):
        cls = name.split(".")[0]
        if "." in name and cls in starter_classes:
            r.errors.append(f"в starter.py у класса {cls} нет метода {name.split('.')[1]}, который есть в solution.py — объявите его в заготовке")
    if not any(isinstance(n, (ast.FunctionDef, ast.ClassDef)) for n in starter.body):
        r.errors.append("starter.py не объявляет ни одной функции")

    test_fns = [n for n in tests.body if isinstance(n, ast.FunctionDef) and n.name.startswith("test_")]
    names = [n.name for n in test_fns]
    if len(test_fns) < MIN_TESTS:
        r.errors.append(f"tests.py: тестов {len(test_fns)}, нужно не меньше {MIN_TESTS}")
    for dup in {n for n in names if names.count(n) > 1}:
        r.errors.append(f"tests.py: функция {dup} объявлена дважды — первая молча не запустится")
    for fn in test_fns:
        if not ast.get_docstring(fn):
            r.errors.append(f"tests.py: у {fn.name} нет docstring — его текст выводится в ✓/✗")

    own = {n.name for n in tests.body if isinstance(n, (ast.FunctionDef, ast.ClassDef))}
    used = {n.id for n in ast.walk(tests) if isinstance(n, ast.Name)}
    for name in sorted((used & sol_sig.keys()) - s_sig.keys() - own):
        r.errors.append(f"tests.py использует {name}, которого нет в starter.py — у пользователя будет NameError")
    # атрибуты и методы классов решения, к которым обращаются тесты, должны быть видны и в заготовке
    attrs = {n.attr for n in ast.walk(tests) if isinstance(n, ast.Attribute)}
    own_members = class_members(tests)
    for name in sorted((attrs & class_members(solution)) - class_members(starter) - own_members):
        r.errors.append(f"tests.py обращается к .{name}, которого нет в классах starter.py — объявите метод или атрибут в заготовке")
    if (r.path / DATA_FILE).exists():
        data = parse_py(r, DATA_FILE)
        if data is not None:
            lines = len((r.path / DATA_FILE).read_text("utf-8").strip().splitlines())
            if lines > DATA_MAX_LINES:
                r.errors.append(f"{DATA_FILE}: {lines} строк, не больше {DATA_MAX_LINES} — данные строятся кодом, а не хранятся таблицей")
            clash = {n.name for n in data.body if isinstance(n, (ast.FunctionDef, ast.ClassDef))} & (s_sig.keys() | own)
            for name in sorted(clash):
                r.errors.append(f"{DATA_FILE}: {name} объявлен и в данных, и в заготовке или тестах")

    starter_src = (r.path / "starter.py").read_text("utf-8")
    solution_src = (r.path / "solution.py").read_text("utf-8")
    task_type = r.meta.get("type")
    if task_type == "implement" and "raise NotImplementedError" not in starter_src:
        r.errors.append("implement: тело заготовки должно быть raise NotImplementedError (иначе тесты проходят «даром»)")
    for alt in alt_files(r):
        tree = parse_py(r, f"{ALT_DIR}/{alt.name}")
        if tree is None:
            continue
        alt_sig = signatures(tree)
        for name, sig in s_sig.items():
            if alt_sig.get(name) != sig:
                r.errors.append(f"{ALT_DIR}/{alt.name}: {name} отсутствует или сигнатура отличается от starter.py")
    if starter_src.strip() == solution_src.strip():
        r.errors.append("starter.py совпадает с solution.py")
    if task_type == "complete":
        if "# TODO" not in starter_src:
            r.errors.append("complete: в starter.py нет пометок # TODO")
        if "# TODO" in solution_src:
            r.errors.append("complete: в solution.py остались # TODO")
    if task_type == "fix-bug":
        diff = [
            line
            for line in difflib.unified_diff(starter_src.splitlines(), solution_src.splitlines(), lineterm="", n=0)
            if line[:1] in "+-" and not line.startswith(("+++", "---"))
        ]
        if not diff:
            r.errors.append("fix-bug: starter.py и solution.py отличаются только пробелами")
        elif len(diff) > 12:
            r.warnings.append(f"fix-bug: отличается {len(diff)} строк — это точно тот же код с точечными ошибками?")
    return True


# ─── Запуск тестов ──────────────────────────────────────────────────────────

PROBE = f"""
import json, os, runpy, sys, warnings
g = runpy.run_path(sys.argv[1], run_name="__bundle__")
if sys.argv[2:] == ["strict"]:  # эталон: устаревший API — ошибка теста, а не тихое предупреждение
    warnings.filterwarnings("error", category=DeprecationWarning)
    warnings.filterwarnings("error", category=FutureWarning)
    pandas_errors = sys.modules.get("pandas.errors")
    if pandas_errors is not None and hasattr(pandas_errors, "SettingWithCopyWarning"):
        warnings.filterwarnings("error", category=pandas_errors.SettingWithCopyWarning)
print({RESULT_MARK!r} + json.dumps(g["_run_tests"](verbose=False), ensure_ascii=False), flush=True)
os._exit(0)  # зависший тест остаётся в фоновом потоке — не ждём его
"""


def run_bundle(source: str, strict: bool = False) -> tuple[list | None, str]:
    """Возвращает (результаты тестов, текст ошибки). strict — Deprecation/FutureWarning в тестах становятся ошибками."""
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False, encoding="utf-8") as f:
        f.write(source)
        path = f.name
    env = {**os.environ, "PYTHONIOENCODING": "utf-8", "PYTHONDONTWRITEBYTECODE": "1"}
    try:
        proc = subprocess.run(
            [sys.executable, "-c", PROBE, path, *(["strict"] if strict else [])], capture_output=True, text=True, timeout=TIMEOUT, env=env
        )
    except subprocess.TimeoutExpired:
        return None, f"завис: не завершился за {TIMEOUT} с"
    finally:
        os.unlink(path)
    for line in reversed(proc.stdout.splitlines()):
        if line.startswith(RESULT_MARK):
            results = json.loads(line[len(RESULT_MARK):])
            return [(r["title"], r["status"] == "passed", r["message"]) for r in results], ""
    err = proc.stderr.strip().splitlines()
    return None, "упал при загрузке: " + (err[-1] if err else f"код выхода {proc.returncode}")


def run_as_script(source: str) -> str:
    """Запускает сборку как обычный скрипт и возвращает последнюю строку вывода."""
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False, encoding="utf-8") as f:
        f.write(source)
        path = f.name
    env = {**os.environ, "PYTHONIOENCODING": "utf-8", "PYTHONDONTWRITEBYTECODE": "1"}
    try:
        proc = subprocess.run([sys.executable, path], capture_output=True, text=True, timeout=TIMEOUT, env=env)
    except subprocess.TimeoutExpired:
        return ""
    finally:
        os.unlink(path)
    lines = proc.stdout.strip().splitlines()
    return lines[-1] if lines else ""


def check_runs(r: TaskReport) -> None:
    solution = build_bundle(r.path, "solution.py")
    results, err = run_bundle(solution, strict=True)
    if results is None:
        r.errors.append(f"solution: {err}")
    else:
        failed = [(t, m) for t, ok, m in results if not ok]
        r.solution_result = f"{len(results) - len(failed)}/{len(results)}"
        for title, message in failed:
            r.errors.append(f"solution не проходит тест «{title}»: {message}")
        last = run_as_script(solution)
        if not last.startswith(f"Прошло {len(results)} из {len(results)}"):
            r.errors.append(f"запуск solution как скрипта: ожидался итог «Прошло N из N», получено {last!r}")

    results, err = run_bundle(build_bundle(r.path, "starter.py"))
    if results is None:
        r.errors.append(f"starter: {err} (заготовка должна запускаться и просто не проходить тесты)")
    else:
        failed = sum(not ok for _, ok, _ in results)
        r.starter_result = f"{len(results) - failed}/{len(results)}"
        if failed == 0:
            r.errors.append("starter.py проходит все тесты — ошибка/пропуск не ловится тестами")

    alts = alt_files(r)
    passed_alts = 0
    for alt in alts:
        results, err = run_bundle(build_bundle(r.path, code=alt.read_text("utf-8")), strict=True)
        if results is None:
            r.errors.append(f"{ALT_DIR}/{alt.name}: {err}")
            continue
        failed = [(t, m) for t, ok, m in results if not ok]
        for title, message in failed:
            r.errors.append(f"{ALT_DIR}/{alt.name} (корректное решение) не проходит тест «{title}»: {message}")
        passed_alts += not failed
    if alts:
        r.alt_result = f"{passed_alts}/{len(alts)}"

    check_mutants(r)
    if r.meta.get("type") == "fix-bug":
        check_each_bug(r)


def check_mutants(r: TaskReport) -> None:
    path = r.path / MUTANTS_FILE
    if not path.exists():
        return
    try:
        mutants = load_toml(path).get("mutant", [])
    except tomllib.TOMLDecodeError as e:
        r.errors.append(f"{MUTANTS_FILE} не парсится: {e}")
        return
    solution = (r.path / "solution.py").read_text("utf-8")
    caught = 0
    for m in mutants:
        name, find, replace = m.get("name", "?"), m.get("find", ""), m.get("replace", "")
        if not find or find not in solution:
            r.errors.append(f"мутант «{name}»: фрагмент {find!r} не найден в solution.py")
            continue
        results, err = run_bundle(build_bundle(r.path, code=solution.replace(find, replace, 1)))
        if results is not None and all(ok for _, ok, _ in results):
            r.errors.append(f"мутант «{name}» проходит все тесты — добавьте тест, который ловит эту ошибку")
        else:
            caught += 1
    r.mutant_result = f"{caught}/{len(mutants)}"


def alt_files(r: TaskReport) -> list[Path]:
    folder = r.path / ALT_DIR
    return sorted(folder.glob("*.py")) if folder.is_dir() else []


def check_each_bug(r: TaskReport) -> None:
    """Каждая ошибка по отдельности должна ловиться тестами — иначе исправление одной «прячет» другую."""
    starter = (r.path / "starter.py").read_text("utf-8").splitlines(keepends=True)
    solution = (r.path / "solution.py").read_text("utf-8").splitlines(keepends=True)
    ops = []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, solution, starter).get_opcodes():
        if tag == "replace" and i2 - i1 == j2 - j1:  # соседние изменённые строки — отдельные ошибки
            ops += [("replace", i1 + k, i1 + k + 1, j1 + k, j1 + k + 1) for k in range(i2 - i1)]
        else:
            ops.append((tag, i1, i2, j1, j2))
    changed = [n for n, op in enumerate(ops) if op[0] != "equal"]

    # перенесённая строка (удалена в одном месте, вставлена в другом) — одна ошибка
    bugs: list[set[int]] = []
    used: set[int] = set()
    for a in changed:
        if a in used:
            continue
        group = {a}
        if ops[a][0] == "delete":
            text = "".join(solution[ops[a][1]:ops[a][2]]).strip()
            for b in changed:
                if b not in used and b != a and ops[b][0] == "insert" and "".join(starter[ops[b][3]:ops[b][4]]).strip() == text:
                    group.add(b)
                    break
        used |= group
        bugs.append(group)

    if len(bugs) > r.meta.get("bugs", 0):
        r.warnings.append(f"fix-bug: мест с отличиями {len(bugs)}, а bugs = {r.meta.get('bugs')}")
    if len(bugs) < 2:
        return
    for group in bugs:
        variant = "".join(
            "".join(starter[j1:j2] if n in group else solution[i1:i2]) for n, (_, i1, i2, j1, j2) in enumerate(ops)
        )
        results, err = run_bundle(build_bundle(r.path, code=variant))
        first = ops[min(group)]
        where = "".join(starter[first[3]:first[4]]).strip() or f"удалены строки {first[1] + 1}–{first[2]} решения"
        if results is not None and all(ok for _, ok, _ in results):
            r.errors.append(f"fix-bug: ошибка «{where}» сама по себе не ловится тестами")


def check_complexity_code(r: TaskReport) -> None:
    parse_py(r, "code.py")


# ─── Обход ──────────────────────────────────────────────────────────────────


def validate_task(task_dir: Path, book_code: str, packages: frozenset[str] = frozenset()) -> TaskReport:
    r = TaskReport(task_dir)
    if not SLUG_RE.match(task_dir.name):
        r.errors.append(f"имя папки задачи должно быть в kebab-case: {task_dir.name}")
    check_meta(r, book_code)
    if not r.meta or r.meta.get("type") not in TYPES:
        return r
    if not check_files(r):
        return r
    check_task_md(r)
    if r.meta["type"] == "complexity":
        check_complexity_code(r)
        return r
    if check_code(r):
        check_imports(r, packages)
    if not r.errors:
        check_runs(r)
    return r


def check_imports(r: TaskReport, packages: frozenset[str]) -> None:
    """В задачах по книгам — только стандартная библиотека; в задачах темы ещё и её пакеты."""
    allowed = set(sys.stdlib_module_names) | set(packages)
    for name in ("starter.py", "solution.py", "tests.py", DATA_FILE, *(f"{ALT_DIR}/{p.name}" for p in alt_files(r))):
        path = r.path / name
        if not path.exists():
            continue
        for node in ast.walk(ast.parse(path.read_text("utf-8"))):
            modules = [a.name for a in node.names] if isinstance(node, ast.Import) else (
                [node.module] if isinstance(node, ast.ImportFrom) and node.module and not node.level else [])
            for module in modules:
                top = module.split(".")[0]
                if top not in allowed:
                    where = "этом разделе — только стандартная библиотека (packages пуст)" if not packages else f"теме разрешены {', '.join(sorted(packages))} и стандартная библиотека"
                    r.errors.append(f"{name}: import {module} — в {where}")


_lessons: set[str] | None = None


def course_lessons() -> set[str]:
    """id уроков курсов из frontmatter courses/<курс>/<модуль>/<урок>/lesson.mdx — для поля lessons."""
    global _lessons
    if _lessons is None:
        _lessons = set()
        for mdx in (CONTENT / "courses").glob("*/*/*/lesson.mdx"):
            front = mdx.read_text("utf-8").split("---")
            m = re.search(r"^id:\s*['\"]?([a-z0-9-]+)", front[1] if len(front) > 2 else "", re.M)
            if m:
                _lessons.add(m[1])
    return _lessons


def reference_articles() -> set[str]:
    """id статей справочника («numpy/broadcasting») по оглавлениям reference/*/topic.toml."""
    ids: set[str] = set()
    for topic_path in (CONTENT / "reference").glob("*/topic.toml"):
        for section in load_toml(topic_path).get("sections", []):
            ids.update(f"{topic_path.parent.name}/{slug}" for slug in section.get("articles", []))
    return ids


def load_meta_file(path: Path, required: set[str], optional: set[str], errors: list[str]) -> dict:
    try:
        data = load_toml(path)
    except FileNotFoundError:
        errors.append(f"нет {path.relative_to(ROOT)}")
        return {}
    except tomllib.TOMLDecodeError as e:
        errors.append(f"{path.relative_to(ROOT)} не парсится: {e}")
        return {}
    check_keys(data, required, optional, str(path.relative_to(ROOT)), errors)
    return data


SELF_CHECKS = {
    "бесконечный цикл": (
        "def spin() -> None:\n    while True:\n        pass\n",
        'def test_before():\n    """До зависания"""\n\n\ndef test_hang():\n    """Зависает"""\n    spin()\n\n\n'
        'test_hang.timeout = 1\n\n\ndef test_after():\n    """После зависания"""\n',
    ),
    "бесконечная рекурсия": (
        "def dive(n: int) -> int:\n    return dive(n + 1)\n",
        'def test_dive():\n    """Уходит в бесконечную рекурсию"""\n    dive(0)\n',
    ),
    "функция test_ в решении": (
        "def test_my_idea() -> None:\n    raise AssertionError('своя проверка, а не тест задачи')\n\n\n"
        "def add(a: int, b: int) -> int:\n    return a + b\n",
        'def test_add():\n    """add(2, 3) == 5"""\n    assert add(2, 3) == 5\n',
    ),
    "глубокая рекурсия через C-вызовы": (
        "import sys\n\n\ndef depth(n: int) -> int:\n    return 0 if n == 0 else 1 + max(map(depth, [n - 1]))\n",
        'def test_deep():\n    """20 000 уровней при поднятом лимите рекурсии"""\n'
        '    sys.setrecursionlimit(30_000)\n    assert depth(20_000) == 20_000\n',
    ),
}


def self_check_bundle(name: str, runner: str) -> str:
    code, tests = SELF_CHECKS[name]
    return f"{code}\n\n{tests}\n\n{tests_list(tests)}\n\n{runner}"


def check_runner() -> list[str]:
    """Раннер не должен зависать и падать: проверка на синтетических «задачах»."""
    runner = RUNNER.read_text("utf-8")
    bundle = lambda name: self_check_bundle(name, runner)
    errors = []

    source = bundle("бесконечный цикл")
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False, encoding="utf-8") as f:
        f.write(source)
        path = f.name
    env = {**os.environ, "PYTHONIOENCODING": "utf-8", "PYTHONDONTWRITEBYTECODE": "1"}
    try:
        proc = subprocess.run([sys.executable, path], capture_output=True, text=True, timeout=10, env=env)
        out = proc.stdout
        if not ("✓ До зависания" in out and "не завершился за 1 с" in out and "– После зависания" in out):
            errors.append(f"раннер: при зависшем тесте ожидался итог с пометками, получено: {out[-300:]!r}")
    except subprocess.TimeoutExpired:
        errors.append("раннер: скрипт с бесконечным циклом не завершился сам за 10 с")
    finally:
        os.unlink(path)

    results, err = run_bundle(bundle("бесконечная рекурсия"))
    if results is None or not results[0][2].startswith("RecursionError"):
        errors.append(f"раннер: бесконечная рекурсия должна давать RecursionError, получено {results or err!r}")

    results, err = run_bundle(bundle("функция test_ в решении"))
    if results != [("add(2, 3) == 5", True, "")]:
        errors.append(f"раннер: функция test_… из кода решения не должна запускаться как тест, получено {results or err!r}")

    results, err = run_bundle(bundle("глубокая рекурсия через C-вызовы"))
    if results is None:
        errors.append(f"раннер: глубокая рекурсия аварийно завершила Python ({err})")
    elif not (results[0][1] or results[0][2].startswith("RecursionError")):
        errors.append(f"раннер: глубокая рекурсия — неожиданный результат {results[0]!r}")
    return errors


def export_bundles(out: Path) -> int:
    """Готовые копируемые файлы с эталоном и альтернативными эталонами — их гоняет CI на разных ОС и версиях."""
    out.mkdir(parents=True, exist_ok=True)
    count = 0
    for meta_path in sorted(CHALLENGES.glob("*/*/*/meta.toml")):
        task_dir = meta_path.parent
        meta = load_toml(meta_path)
        if meta.get("type") == "complexity":
            continue
        (out / f"{meta['id']}__solution.py").write_text(build_bundle(task_dir, "solution.py"), "utf-8")
        count += 1
        for alt in sorted((task_dir / ALT_DIR).glob("*.py")) if (task_dir / ALT_DIR).is_dir() else []:
            code = alt.read_text("utf-8")
            (out / f"{meta['id']}__alt_{alt.stem}.py").write_text(build_bundle(task_dir, code=code), "utf-8")
            count += 1
    runner = RUNNER.read_text("utf-8")
    for name, key in (("hang", "бесконечный цикл"), ("recursion", "бесконечная рекурсия"), ("user_test", "функция test_ в решении"), ("deep", "глубокая рекурсия через C-вызовы")):
        (out / f"selfcheck__{name}.py").write_text(self_check_bundle(key, runner), "utf-8")
        count += 1
    print(f"Собрано файлов: {count} → {out}")
    return 0


def collect_ids() -> dict[str, list[Path]]:
    ids: dict[str, list[Path]] = {}
    for meta_path in CHALLENGES.glob("*/*/*/meta.toml"):
        try:
            task_id = load_toml(meta_path).get("id")
        except tomllib.TOMLDecodeError:
            continue
        if isinstance(task_id, str):
            ids.setdefault(task_id, []).append(meta_path.parent)
    return ids


def check_book_kind(book: dict, book_dir: Path, errors: list[str]) -> frozenset[str]:
    """Проверяет поля раздела задач и возвращает разрешённые пакеты (пусто — только stdlib)."""
    where = f"{book_dir.name}/book.toml"
    kind = book.get("kind", "book")
    if "direction" in book and book["direction"] not in DIRECTIONS:
        errors.append(f"{where}: direction — одно из {', '.join(DIRECTIONS)}")
    if not isinstance(book.get("beta", False), bool):
        errors.append(f"{where}: beta — true или false")
    if kind not in BOOK_KINDS:
        errors.append(f"{where}: kind — одно из {', '.join(BOOK_KINDS)}")
        return frozenset()
    packages = book.get("packages", [])
    if kind == "book":
        if "author" not in book:
            errors.append(f"{where}: у книги нужно поле author")
        if packages:
            errors.append(f"{where}: задачи по книгам работают на стандартной библиотеке — packages не нужен")
        return frozenset()
    # packages = [] — тема на стандартной библиотеке (ООП): как книга, но с reference и подписью «Раздел»
    if "packages" not in book or not is_str_list(packages) or not set(packages) <= KNOWN_PACKAGES:
        errors.append(f"{where}: у темы нужен packages — список из {', '.join(sorted(KNOWN_PACKAGES))} или [] (только стандартная библиотека)")
        return frozenset()
    reference = book.get("reference")
    if reference is not None and not (CONTENT / "reference" / str(reference) / "topic.toml").exists():
        errors.append(f"{where}: reference = {reference!r} — такой темы справочника нет")
    return frozenset(packages)


def main() -> int:
    parser = argparse.ArgumentParser(description="Валидация задач в challenges/")
    parser.add_argument("--book", help="папка книги, например grokking-algorithms")
    parser.add_argument("--chapter", help="папка главы, например 03-recursion")
    parser.add_argument("--bundle", type=Path, help="напечатать собранный .py для задачи и выйти")
    parser.add_argument("--solution", action="store_true", help="с --bundle: собрать с solution.py")
    parser.add_argument("--export", type=Path, help="собрать файлы с solution.py и alt_solutions в папку (для CI) и выйти")
    args = parser.parse_args()

    if args.export:
        return export_bundles(args.export)

    if args.bundle:
        print(build_bundle(args.bundle.resolve(), "solution.py" if args.solution else "starter.py"), end="")
        return 0

    global_errors: list[str] = check_runner()
    reports: dict[Path, list[TaskReport]] = {}
    chapter_warnings: dict[Path, list[str]] = {}
    all_ids = collect_ids()  # по всем книгам, даже если проверяется одна глава

    books = sorted(p for p in CHALLENGES.iterdir() if p.is_dir()) if CHALLENGES.exists() else []
    for book_dir in books:
        if args.book and book_dir.name != args.book:
            continue
        if not SLUG_RE.match(book_dir.name) or book_dir.name == "reference":
            global_errors.append(f"недопустимое имя папки книги: {book_dir.name}")
        book = load_meta_file(book_dir / "book.toml", BOOK_REQUIRED, BOOK_OPTIONAL, global_errors)
        code = book.get("code", "?")
        packages = check_book_kind(book, book_dir, global_errors)
        for chapter_dir in sorted(p for p in book_dir.iterdir() if p.is_dir()):
            if args.chapter and chapter_dir.name != args.chapter:
                continue
            if not CHAPTER_DIR_RE.match(chapter_dir.name):
                global_errors.append(f"папка главы должна называться NN-slug: {chapter_dir.relative_to(ROOT)}")
                continue
            load_meta_file(chapter_dir / "chapter.toml", CHAPTER_REQUIRED, CHAPTER_OPTIONAL, global_errors)
            task_dirs = sorted(p for p in chapter_dir.iterdir() if p.is_dir() and p.name not in IGNORED_FILES)
            chapter_reports = [validate_task(t, code, packages) for t in task_dirs]
            for rep in chapter_reports:
                task_id = rep.meta.get("id")
                others = [p for p in all_ids.get(task_id, []) if p != rep.path]
                if others:
                    rep.errors.append(f"id {task_id} уже занят: {', '.join(str(p.relative_to(ROOT)) for p in others)}")
            reports[chapter_dir] = chapter_reports

            warns = []
            n = len(chapter_reports)
            if not 6 <= n <= 10:
                warns.append(f"задач в главе {n}, ожидается 6–10")
            diffs = Counter(rep.meta.get("difficulty") for rep in chapter_reports)
            for d in DIFFICULTIES:
                if not diffs[d]:
                    warns.append(f"нет задач сложности {d}")
            if len({rep.meta.get("type") for rep in chapter_reports}) < 2:
                warns.append("в главе меньше двух типов задач")
            chapter_warnings[chapter_dir] = warns

    print_summary(reports, chapter_warnings, global_errors)
    has_errors = global_errors or any(not rep.ok for reps in reports.values() for rep in reps)
    return 1 if has_errors else 0


def print_summary(
    reports: dict[Path, list[TaskReport]], chapter_warnings: dict[Path, list[str]], global_errors: list[str]
) -> None:
    green, red, yellow, dim, reset = "\033[32m", "\033[31m", "\033[33m", "\033[2m", "\033[0m"
    if not sys.stdout.isatty():
        green = red = yellow = dim = reset = ""

    total = ok = 0
    for chapter_dir, reps in reports.items():
        print(f"\n{chapter_dir.relative_to(CHALLENGES)}")
        for rep in reps:
            total += 1
            ok += rep.ok
            mark = f"{green}✓{reset}" if rep.ok else f"{red}✗{reset}"
            m = rep.meta
            runs = ""
            if rep.solution_result or rep.starter_result:
                runs = f"{dim}solution {rep.solution_result or '—'} · starter {rep.starter_result or '—'}"
                runs += f" · alt {rep.alt_result}" if rep.alt_result else ""
                runs += (f" · мутанты {rep.mutant_result}" if rep.mutant_result else "") + reset
            elif m.get("type") == "complexity":
                runs = f"{dim}ответ: {m.get('complexity', {}).get('answer', '?')}{reset}"
            print(f"  {mark} {rep.path.name:<26} {str(m.get('difficulty', '?')):<7} {str(m.get('type', '?')):<11} {runs}")
            for e in rep.errors:
                print(f"      {red}ошибка:{reset} {e}")
            for w in rep.warnings:
                print(f"      {yellow}внимание:{reset} {w}")
        diffs = Counter(rep.meta.get("difficulty") for rep in reps)
        types = Counter(rep.meta.get("type") for rep in reps)
        print(
            f"  {dim}итого {len(reps)}: "
            + ", ".join(f"{d} {diffs[d]}" for d in DIFFICULTIES)
            + " · "
            + ", ".join(f"{t} {types[t]}" for t in TYPES if types[t])
            + reset
        )
        for w in chapter_warnings.get(chapter_dir, []):
            print(f"  {yellow}внимание:{reset} {w}")

    for e in global_errors:
        print(f"\n{red}ошибка:{reset} {e}")
    color = green if ok == total and not global_errors else red
    print(f"\n{color}Валидацию прошли {ok} из {total} задач{reset}")


if __name__ == "__main__":
    sys.exit(main())

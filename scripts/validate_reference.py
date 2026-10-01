#!/usr/bin/env python3
"""Проверка справочника: структура статей, ссылки и выполнение примеров.

    .venv/bin/python scripts/validate_reference.py                  # проверить всё
    .venv/bin/python scripts/validate_reference.py --update         # перезаписать вывод примеров
    .venv/bin/python scripts/validate_reference.py numpy/broadcasting pandas   # только выбранное
    .venv/bin/python scripts/validate_reference.py --strict         # ошибка, если статья из оглавления не написана
    .venv/bin/python scripts/validate_reference.py --update --retime   # заново снять все замеры времени

Нужны NumPy и pandas ровно тех версий, что в requirements-dev.txt: вывод примеров зависит от версии.

Формат файла примеров (reference/<тема>/<статья>.py) — ячейки в стиле «# %%»:

    # %% setup                      ← необязательные общие данные; выполняются перед каждым примером
    # %% <id>                       ← пример; <Example id="<id>" /> в статье
    # %% <id> [raises=ValueError]   ← пример обязан упасть с этим исключением
    # %% <id> [warns]               ← пример может выдавать предупреждения (кроме Deprecation/Future)
    # %% <id> [norun]               ← не выполняется, только проверка синтаксиса
    # %% <id> [deprecated]          ← показывает устаревший API: DeprecationWarning/FutureWarning обязателен
    # %% <id> [timing]              ← замер времени: выполняется, но числа в выводе не сравниваются
    # ─── вывод ───                  ← дальше вывод, каждая строка с префиксом «# »; пишет --update

Пример выполняется как ячейка Jupyter: печатается stdout, затем repr последнего выражения (если не None).
Перед каждым примером выполняются reference/prelude.py (импорты и настройки отображения) — или свой prelude
темы reference/<тема>/prelude.py, если он есть (у тем без пакета: ООП, алгоритмы), — и setup статьи;
пространство имён и временная рабочая папка у каждого примера свои.

Замеры времени. --update записывает вывод примера [timing] вместе с машиной и датой:
[timing=2026-09-29, machine=Apple M3 Pro · macOS · Python 3.14]. Дальше числа не сравниваются — только
текст вокруг них; замер переснимается, если текст изменился, или по --retime.

Графики. Фигуры matplotlib, оставшиеся открытыми после примера, сохраняются в SVG (тёмная тема сайта)
в public/reference/plots/<тема>/<статья>/<id>.svg и сравниваются с сохранёнными, как текстовый вывод.
Объект осей, который вернул .plot, в текстовый вывод не попадает — вместо него статья показывает график.
"""

from __future__ import annotations

import contextlib
import difflib
import os
import platform
import re
import subprocess
import sys
import tomllib
import traceback
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# EDU_CONTENT_ROOT — другая папка с той же структурой (образцы платформы tests/platform), как в src/lib/paths.ts
CONTENT = (ROOT / os.environ["EDU_CONTENT_ROOT"]).resolve() if os.environ.get("EDU_CONTENT_ROOT") else ROOT
REFERENCE = CONTENT / "reference"
PRELUDE = ROOT / "reference" / "prelude.py"  # общий; у темы может быть свой reference/<тема>/prelude.py
REQUIREMENTS = ROOT / "requirements-dev.txt"
PLOTS = CONTENT / "public" / "reference" / "plots"
DIRECTIONS = ("python", "data", "git", "english")  # как DIRECTIONS в src/lib/directions.ts

sys.path.insert(0, str(ROOT / "runtime"))
from reference_exec import ExampleRunner  # noqa: E402 — общий с сайтом запуск примеров

OUTPUT_MARK = "# ─── вывод ───"
FLAGS = {"raises", "warns", "norun", "deprecated", "timing", "machine"}
NUMBER_RE = re.compile(r"\d+(?:[.,]\d+)?")
CELL_RE = re.compile(r"^# %% ([a-z0-9]+(?:-[a-z0-9]+)*)(?: \[([^\]]*)\])?$")
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LEVELS = ("basic", "medium", "advanced")
KINDS = ("article", "overview")  # overview — свободная структура: частые ошибки, шпаргалка
FRONTMATTER_REQUIRED = {"title", "level", "summary"}  # docs — обязателен у статей темы с пакетом
FRONTMATTER_OPTIONAL = {"requires", "related", "functions", "kind", "docs", "practice"}
LIST_KEYS = {"requires", "related", "functions", "practice"}
ADDRESS_RE = re.compile(r"\bat 0x[0-9a-fA-F]{6,}")  # repr объекта без __repr__: адрес меняется от запуска к запуску
# Разделы статьи в порядке следования: обязательные и необязательные.
SECTIONS_REQUIRED = ("Коротко", "Примеры", "Подводные камни")
SECTIONS_ORDER = ("Коротко", "Синтаксис", "Параметры", "Примеры", "Подводные камни")
FORBIDDEN_WARNINGS = (DeprecationWarning, PendingDeprecationWarning, FutureWarning)

# ─── Файл примеров ──────────────────────────────────────────────────────────


@dataclass
class Cell:
    id: str
    flags: dict[str, str]
    code: str
    output: list[str] | None  # None — блока вывода нет
    line: int


@dataclass
class ExamplesFile:
    preamble: list[str]
    cells: list[Cell]

    def get(self, cell_id: str) -> Cell | None:
        return next((c for c in self.cells if c.id == cell_id), None)


def parse_flags(text: str | None) -> dict[str, str]:
    flags: dict[str, str] = {}
    for part in filter(None, (p.strip() for p in (text or "").split(","))):
        key, _, value = part.partition("=")
        flags[key.strip()] = value.strip()
    return flags


def parse_examples(text: str) -> ExamplesFile:
    lines = text.splitlines()
    preamble: list[str] = []
    cells: list[Cell] = []
    current: dict | None = None

    def finish():
        if current is None:
            return
        code = current["code"]
        while code and not code[-1].strip():
            code.pop()
        out = current["out"]
        if out is not None:
            while out and not out[-1].strip():
                out.pop()
            out = [strip_comment(l, current["line"]) for l in out]
        cells.append(Cell(current["id"], current["flags"], "\n".join(code), out, current["line"]))

    for number, line in enumerate(lines, 1):
        m = CELL_RE.match(line)
        if m:
            finish()
            current = {"id": m[1], "flags": parse_flags(m[2]), "code": [], "out": None, "line": number}
        elif line.startswith("# %%"):
            raise ValueError(f"строка {number}: неверный заголовок ячейки «{line}» — нужно «# %% id» или «# %% id [флаги]»")
        elif current is None:
            preamble.append(line)
        elif line == OUTPUT_MARK:
            if current["out"] is not None:
                raise ValueError(f"строка {number}: второй блок вывода в ячейке {current['id']}")
            current["out"] = []
        elif current["out"] is not None:
            current["out"].append(line)
        else:
            current["code"].append(line)
    finish()
    return ExamplesFile(preamble, cells)


def strip_comment(line: str, cell_line: int) -> str:
    if line == "#":
        return ""
    if line.startswith("# "):
        return line[2:]
    if not line.strip():
        return ""
    raise ValueError(f"ячейка на строке {cell_line}: строка вывода без префикса «# »: {line!r}")


def serialize_examples(ex: ExamplesFile) -> str:
    parts = ["\n".join(ex.preamble).rstrip("\n")] if any(l.strip() for l in ex.preamble) else []
    for cell in ex.cells:
        flags = ", ".join(f"{k}={v}" if v else k for k, v in cell.flags.items())
        chunk = [f"# %% {cell.id}" + (f" [{flags}]" if flags else "")]
        if cell.code:
            chunk.append(cell.code)
        if cell.output is not None:
            chunk.append(OUTPUT_MARK)
            chunk.extend(f"# {l}" if l else "#" for l in cell.output)
        parts.append("\n".join(chunk))
    return "\n\n".join(parts) + "\n"


# ─── Выполнение ─────────────────────────────────────────────────────────────
# Сам запуск примера — в runtime/reference_exec.py: тот же код выполняет примеры на сайте (Pyodide).


TOPICS: dict[str, dict] = {}  # topic.toml по имени темы — заполняет main()


def own_prelude(topic: str) -> Path | None:
    """Свой prelude темы (reference/<тема>/prelude.py) — выполняется вместо общего reference/prelude.py."""
    path = REFERENCE / topic / "prelude.py"
    return path if path.exists() else None


_runners: dict[Path, ExampleRunner] = {}


def make_runner(topic: str) -> ExampleRunner:
    path = own_prelude(topic) or PRELUDE
    if path not in _runners:
        _runners[path] = ExampleRunner(path.read_text(encoding="utf-8"), str(path.relative_to(ROOT)))
    return _runners[path]


_task_ids: set[str] | None = None


def task_ids() -> set[str]:
    """id всех задач (challenges/*/*/*/meta.toml) — для поля practice."""
    global _task_ids
    if _task_ids is None:
        _task_ids = set()
        for meta_path in (CONTENT / "challenges").glob("*/*/*/meta.toml"):
            with contextlib.suppress(tomllib.TOMLDecodeError):
                task_id = tomllib.loads(meta_path.read_text(encoding="utf-8")).get("id")
                if isinstance(task_id, str):
                    _task_ids.add(task_id)
    return _task_ids


def machine_label() -> str:
    """«Apple M3 Pro · macOS · Python 3.14» — где снят замер времени."""
    system = platform.system()
    cpu = ""
    with contextlib.suppress(OSError, subprocess.SubprocessError):
        if system == "Darwin":
            cpu = subprocess.run(["sysctl", "-n", "machdep.cpu.brand_string"], capture_output=True, text=True).stdout
        elif system == "Linux":
            cpu = next((l.split(":", 1)[1] for l in Path("/proc/cpuinfo").read_text().splitlines() if l.startswith("model name")), "")
    os_name = {"Darwin": "macOS"}.get(system, system)
    label = f"{cpu.strip() or platform.machine()} · {os_name} · Python {sys.version_info.major}.{sys.version_info.minor}"
    return re.sub(r"[,=\[\]]", " ", label)  # эти символы разделяют флаги ячейки


# ─── Статьи ─────────────────────────────────────────────────────────────────


@dataclass
class Article:
    topic: str
    slug: str
    section: str
    mdx: Path
    meta: dict = field(default_factory=dict)
    body: str = ""

    @property
    def id(self) -> str:
        return f"{self.topic}/{self.slug}"

    @property
    def examples_path(self) -> Path:
        return self.mdx.with_suffix(".py")


@dataclass
class Report:
    errors: list[str] = field(default_factory=list)
    examples: int = 0
    updated: int = 0


def parse_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---\n"):
        raise ValueError("нет frontmatter (--- в начале файла)")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValueError("frontmatter не закрыт строкой ---")
    meta: dict = {}
    for number, line in enumerate(text[4:end].splitlines(), 2):
        if not line.strip():
            continue
        key, sep, value = line.partition(":")
        key, value = key.strip(), value.strip()
        if not sep or not re.fullmatch(r"[a-z]+", key):
            raise ValueError(f"frontmatter, строка {number}: ожидалось «ключ: значение»")
        if value.startswith("["):
            if not value.endswith("]"):
                raise ValueError(f"frontmatter, строка {number}: список должен быть в одну строку: [a, b]")
            meta[key] = [v.strip() for v in value[1:-1].split(",") if v.strip()]
        elif value[:1] in "\"'":
            if len(value) < 2 or value[-1] != value[0]:
                raise ValueError(f"frontmatter, строка {number}: кавычка не закрыта")
            meta[key] = value[1:-1]
        else:
            if ": " in value or " #" in value or value[:1] in "&*!|>%@`{":
                raise ValueError(f"frontmatter, строка {number}: значение с «: », « #» или спецсимволом в начале возьмите в кавычки")
            meta[key] = value
    return meta, text[end + 5:]


def load_topics() -> tuple[dict[str, dict], list[Article], list[str], list[str]]:
    """Возвращает темы, написанные статьи, ошибки и id статей из оглавления, у которых ещё нет файла."""
    topics: dict[str, dict] = {}
    articles: list[Article] = []
    errors: list[str] = []
    planned: list[str] = []
    for topic_dir in sorted(p for p in REFERENCE.iterdir() if p.is_dir() and not p.name.startswith((".", "_"))):
        topic_path = topic_dir / "topic.toml"
        if not topic_path.exists():
            errors.append(f"{topic_dir.name}: нет topic.toml")
            continue
        meta = tomllib.loads(topic_path.read_text(encoding="utf-8"))
        topics[topic_dir.name] = meta
        # тема с пакетом (NumPy, pandas): package, version, docs; без пакета (ООП, алгоритмы): python — минимальная версия
        required = ("package", "version", "docs") if "package" in meta else ("python",)
        for key in ("title", "summary", "direction", "sections", *required):
            if key not in meta:
                errors.append(f"{topic_dir.name}/topic.toml: нет поля {key}")
        if "package" not in meta and "version" in meta:
            errors.append(f"{topic_dir.name}/topic.toml: version бывает только вместе с package")
        if "python" in meta and not re.fullmatch(r"3\.\d+", str(meta["python"])):
            errors.append(f"{topic_dir.name}/topic.toml: python — минимальная версия строкой, например \"3.10\"")
        if "direction" in meta and meta["direction"] not in DIRECTIONS:
            errors.append(f"{topic_dir.name}/topic.toml: direction — одно из {', '.join(DIRECTIONS)}")
        if not isinstance(meta.get("beta", False), bool):
            errors.append(f"{topic_dir.name}/topic.toml: beta — true или false")
        listed: set[str] = set()
        for section in meta.get("sections", []):
            for slug in section.get("articles", []):
                if slug in listed:
                    errors.append(f"{topic_dir.name}: статья {slug} указана в оглавлении дважды")
                listed.add(slug)
                mdx = topic_dir / f"{slug}.mdx"
                if not SLUG_RE.match(slug):
                    errors.append(f"{topic_dir.name}: имя статьи «{slug}» — только a-z, 0-9 и дефисы")
                elif slug == "index":
                    errors.append(f"{topic_dir.name}: имя «index» занято — загрузчик Astro считает index.mdx страницей темы")
                elif not mdx.exists():
                    planned.append(f"{topic_dir.name}/{slug}")
                else:
                    articles.append(Article(topic_dir.name, slug, section.get("title", ""), mdx))
        for mdx in sorted(topic_dir.glob("*.mdx")):
            if mdx.stem not in listed:
                errors.append(f"{topic_dir.name}: файл {mdx.name} не указан в оглавлении topic.toml")
        for py in sorted(topic_dir.glob("*.py")):
            if py.name != "prelude.py" and not py.with_suffix(".mdx").exists():
                errors.append(f"{topic_dir.name}: файл примеров {py.name} без статьи {py.stem}.mdx")
    return topics, articles, errors, planned


def check_article(article: Article, known: set[str], r: Report):
    where = article.id
    try:
        article.meta, article.body = parse_frontmatter(article.mdx.read_text(encoding="utf-8"))
    except ValueError as e:
        r.errors.append(f"{where}: {e}")
        return
    meta = article.meta
    for key in FRONTMATTER_REQUIRED - meta.keys():
        r.errors.append(f"{where}: во frontmatter нет поля {key}")
    for key in meta.keys() - FRONTMATTER_REQUIRED - FRONTMATTER_OPTIONAL:
        r.errors.append(f"{where}: неизвестное поле frontmatter «{key}»")
    for key in LIST_KEYS & meta.keys():
        if not isinstance(meta[key], list):
            r.errors.append(f"{where}: {key} должен быть списком [a, b]")
    for key in meta.keys() - LIST_KEYS:
        if isinstance(meta[key], list):
            r.errors.append(f"{where}: {key} должен быть строкой")
    if meta.get("level") not in LEVELS:
        r.errors.append(f"{where}: level — одно из {', '.join(LEVELS)}")
    kind = meta.get("kind", "article")
    if kind not in KINDS:
        r.errors.append(f"{where}: kind — одно из {', '.join(KINDS)}")
    topic_meta = TOPICS.get(article.topic, {})
    if "docs" in meta or "package" in topic_meta:
        if not str(meta.get("docs", "")).startswith("https://"):
            r.errors.append(f"{where}: docs — ссылка https:// на официальную документацию")
    for task_id in meta.get("practice", []) if isinstance(meta.get("practice"), list) else []:
        if task_id not in task_ids():
            r.errors.append(f"{where}: practice — задачи {task_id} нет в challenges/")
    for key in ("requires", "related"):
        for ref in meta.get(key, []) if isinstance(meta.get(key), list) else []:
            if ref not in known:
                r.errors.append(f"{where}: {key} ссылается на несуществующую статью {ref}")
            if ref == article.id:
                r.errors.append(f"{where}: {key} ссылается на саму статью")
    if len(meta.get("requires", [])) > 3:
        r.errors.append(f"{where}: в «Нужно знать» (requires) не больше 3 статей")

    body = article.body
    if re.search(r"^(import|export)\s", body, re.M):
        r.errors.append(f"{where}: import/export в статье не нужны — компоненты подключает страница")
    for link in re.findall(r"\(/reference/([a-z0-9-]+/[a-z0-9-]+)(?:#[^)]*)?\)", body):
        if link not in known:
            r.errors.append(f"{where}: ссылка на несуществующую статью /reference/{link}")

    headings = re.findall(r"^## (.+?)\s*$", body, re.M)
    if kind == "article":
        for name in SECTIONS_REQUIRED:
            if name not in headings:
                r.errors.append(f"{where}: нет раздела «## {name}»")
        known_order = [h for h in headings if h in SECTIONS_ORDER]
        if known_order != sorted(known_order, key=SECTIONS_ORDER.index):
            r.errors.append(f"{where}: разделы идут не по порядку: {' → '.join(SECTIONS_ORDER)}")
        if headings and headings[0] != "Коротко":
            r.errors.append(f"{where}: статья начинается с раздела «## Коротко»")
    check_examples(article, r)


def check_examples(article: Article, r: Report):
    where = article.id
    used = re.findall(r"<Example\s+id=\"([^\"]+)\"", article.body)
    has_setup_tag = bool(re.search(r"<Setup\s*/>", article.body))
    path = article.examples_path
    if not path.exists():
        if used or has_setup_tag:
            r.errors.append(f"{where}: в статье есть <Example>/<Setup>, но нет файла {path.name}")
        elif article.meta.get("kind", "article") == "article":
            r.errors.append(f"{where}: у статьи нет примеров ({path.name})")
        return
    try:
        ex = parse_examples(path.read_text(encoding="utf-8"))
    except ValueError as e:
        r.errors.append(f"{where}: {path.name}: {e}")
        return
    ids = [c.id for c in ex.cells]
    for dup in {i for i in ids if ids.count(i) > 1}:
        r.errors.append(f"{where}: пример {dup} определён дважды")
    for dup in {i for i in used if used.count(i) > 1}:
        r.errors.append(f"{where}: <Example id=\"{dup}\"> вставлен дважды")
    for cell_id in used:
        if cell_id == "setup":
            r.errors.append(f"{where}: общие данные показываются через <Setup />, а не <Example id=\"setup\">")
        elif cell_id not in ids:
            r.errors.append(f"{where}: <Example id=\"{cell_id}\"> — такого примера нет в {path.name}")
    for cell_id in ids:
        if cell_id != "setup" and cell_id not in used:
            r.errors.append(f"{where}: пример {cell_id} из {path.name} не вставлен в статью")
    if ("setup" in ids) != has_setup_tag:
        r.errors.append(f"{where}: <Setup /> в статье и ячейка setup в {path.name} должны быть вместе")
    for cell in ex.cells:
        unknown = cell.flags.keys() - FLAGS
        if unknown:
            r.errors.append(f"{where}:{cell.id}: неизвестные флаги {', '.join(sorted(unknown))}")
        if "timing" in cell.flags and cell.flags.keys() & {"raises", "norun"}:
            r.errors.append(f"{where}:{cell.id}: замер [timing] не сочетается с raises и norun")
        if "machine" in cell.flags and "timing" not in cell.flags:
            r.errors.append(f"{where}:{cell.id}: machine бывает только у замера [timing]")
        if not cell.code.strip():
            r.errors.append(f"{where}:{cell.id}: пустой пример")
        if cell.id == "setup" and cell.flags:
            r.errors.append(f"{where}: у setup не бывает флагов")
        if not own_prelude(article.topic) and re.search(r"^\s*(import numpy|import pandas)", cell.code, re.M):
            r.errors.append(f"{where}:{cell.id}: numpy и pandas уже импортированы (np, pd) — уберите import")


def run_examples(article: Article, runner: ExampleRunner, update: bool, retime: bool, r: Report):
    path = article.examples_path
    if not path.exists():
        return
    try:
        ex = parse_examples(path.read_text(encoding="utf-8"))
    except ValueError:
        return  # уже сообщено в check_examples
    setup_cell = ex.get("setup")
    setup = setup_cell.code if setup_cell else ""
    rel = path.relative_to(ROOT)
    if setup_cell is not None:
        check = runner.run(setup, "pass", str(rel), "setup-check")
        if check.error is not None or check.lines or check.plots:
            detail = check.lines[-1] if check.lines else "осталась открытая фигура" if check.plots else ""
            r.errors.append(f"{article.id}:setup: общие данные должны выполняться молча и без ошибок: {detail}")
            return
    changed = False
    plots: dict[Path, str] = {}
    for cell in ex.cells:
        if cell.id == "setup":
            continue
        where = f"{article.id}:{cell.id} ({rel}:{cell.line})"
        r.examples += 1
        if "norun" in cell.flags:
            try:
                compile(cell.code, where, "exec")
            except SyntaxError as e:
                r.errors.append(f"{where}: синтаксическая ошибка: {e}")
            if cell.output is not None:
                r.errors.append(f"{where}: у примера [norun] не бывает вывода")
            continue
        result = runner.run(setup, cell.code, str(rel), cell.id)
        lines, error, categories = result.lines, result.error, result.categories
        for n, svg in enumerate(result.plots, 1):
            plots[PLOTS / article.topic / article.slug / (f"{cell.id}.svg" if n == 1 else f"{cell.id}-{n}.svg")] = svg
        expected_error = cell.flags.get("raises")
        if expected_error:
            if error is None:
                r.errors.append(f"{where}: ожидалось исключение {expected_error}, но пример выполнился без ошибок")
            elif expected_error not in {k.__name__ for k in type(error).__mro__}:
                r.errors.append(f"{where}: ожидалось {expected_error}, а возникло {type(error).__name__}: {error}")
        elif error is not None:
            tb = "".join(traceback.format_exception(error)).rstrip().splitlines()[-4:]
            r.errors.append(f"{where}: пример упал:\n      " + "\n      ".join(tb))
        forbidden = sorted({c.__name__ for c in categories if issubclass(c, FORBIDDEN_WARNINGS)})
        if "deprecated" in cell.flags:
            if not forbidden:
                r.errors.append(f"{where}: помечен [deprecated], но DeprecationWarning/FutureWarning нет")
        elif forbidden:
            r.errors.append(f"{where}: устаревший API — предупреждения {', '.join(forbidden)}")
        elif categories and "warns" not in cell.flags:
            names = ", ".join(sorted({c.__name__ for c in categories}))
            r.errors.append(f"{where}: пример выдаёт предупреждения ({names}); если так задумано, пометьте [warns]")
        elif "warns" in cell.flags and not categories:
            r.errors.append(f"{where}: помечен [warns], но предупреждений нет")

        if any(ADDRESS_RE.search(line) for line in lines):
            r.errors.append(f"{where}: в выводе адрес объекта (at 0x…) — он меняется от запуска к запуску; добавьте классу __repr__")
        stored = cell.output or []
        if "timing" in cell.flags:
            # время зависит от машины: сравнивается только текст вокруг чисел
            fresh = list(map(number_mask, lines)) == list(map(number_mask, stored))
            measured = stored and cell.flags["timing"] and cell.flags.get("machine")
            if fresh and measured and not retime:
                continue
            if update or retime:
                cell.output = lines or None
                cell.flags["timing"] = date.today().isoformat()
                cell.flags["machine"] = machine_label()
                changed = True
                r.updated += 1
            else:
                r.errors.append(f"{where}: замер не снят или текст вывода изменился — снимите заново: --update")
            continue
        if lines != stored:
            if update:
                cell.output = lines or None
                changed = True
                r.updated += 1
            else:
                diff = difflib.unified_diff(stored, lines, "на сайте", "при выполнении", lineterm="", n=1)
                r.errors.append(f"{where}: вывод расходится с сохранённым (обновите: --update):\n      " + "\n      ".join(diff))
    if changed:
        path.write_text(serialize_examples(ex), encoding="utf-8")
    sync_plots(article, plots, update, r)


def number_mask(line: str) -> str:
    """Строка вывода без чисел и выравнивания: «цикл:  12.5 мс» → «цикл: # мс»."""
    return " ".join(NUMBER_RE.sub("#", line).split())


def sync_plots(article: Article, plots: dict[Path, str], update: bool, r: Report):
    """Сверяет SVG графиков статьи с сохранёнными; с --update записывает новые и удаляет лишние."""
    folder = PLOTS / article.topic / article.slug
    existing = set(folder.glob("*.svg")) if folder.exists() else set()
    for path, svg in plots.items():
        if path.exists() and path.read_text(encoding="utf-8") == svg:
            continue
        if update:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(svg, encoding="utf-8", newline="\n")
            r.updated += 1
        else:
            state = "расходится с сохранённым" if path.exists() else "не сохранён"
            r.errors.append(f"{article.id}: график {path.relative_to(ROOT)} {state} (обновите: --update)")
    for path in sorted(existing - plots.keys()):
        if update:
            path.unlink()
            r.updated += 1
        else:
            r.errors.append(f"{article.id}: лишний график {path.relative_to(ROOT)} — ни один пример его не строит")
    if update and folder.exists() and not any(folder.iterdir()):
        folder.rmdir()


# ─── Версии ─────────────────────────────────────────────────────────────────


def pinned_versions() -> dict[str, str]:
    pins = {}
    for line in REQUIREMENTS.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^([A-Za-z0-9_.-]+)==([^\s#]+)", line)
        if m:
            pins[m[1].lower()] = m[2]
    return pins


def check_versions(topics: dict[str, dict], errors: list[str]) -> bool:
    import importlib.metadata as md

    pins = pinned_versions()
    ok = True
    for name, pin in pins.items():
        try:
            installed = md.version(name)
        except md.PackageNotFoundError:
            errors.append(f"не установлен {name}=={pin}: pip install -r requirements-dev.txt")
            ok = False
            continue
        if installed != pin:
            errors.append(f"установлен {name} {installed}, а вывод примеров снят с {pin} (requirements-dev.txt)")
            ok = False
    for topic, meta in topics.items():
        package = str(meta.get("package", "")).lower()
        if package and pins.get(package) != meta.get("version"):
            errors.append(f"{topic}/topic.toml: version = {meta.get('version')}, а в requirements-dev.txt {package}=={pins.get(package)}")
    return ok


def github_error(title: str, message: str) -> None:
    """В GitHub Actions ошибка видна аннотацией на странице запуска — логи без входа не открываются."""
    if os.environ.get("GITHUB_ACTIONS") == "true":
        esc = lambda s: s.replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")
        print(f"::error title={esc(title).replace(',', '%2C').replace(':', '%3A')}::{esc(message)}")


# ─── Точка входа ────────────────────────────────────────────────────────────


def main(argv: list[str]) -> int:
    if os.environ.get("PYTHONHASHSEED") != "0":  # порядок элементов set в выводе должен быть одинаковым
        os.environ["PYTHONHASHSEED"] = "0"
        os.execv(sys.executable, [sys.executable, *sys.argv])
    update = "--update" in argv
    retime = "--retime" in argv
    strict = "--strict" in argv
    selected = [a for a in argv if not a.startswith("--")]

    topics, articles, errors, planned = load_topics()
    TOPICS.update(topics)
    known = {a.id for a in articles} | set(planned)  # ссылаться на запланированную статью можно
    runnable = check_versions(topics, errors)

    reports: dict[str, Report] = {}
    for article in articles:
        if selected and not any(article.id == s or article.topic == s for s in selected):
            continue
        r = reports.setdefault(article.id, Report())
        check_article(article, known, r)
        if runnable:
            run_examples(article, make_runner(article.topic), update, retime, r)

    if PLOTS.exists() and not selected:
        written = {a.id for a in articles}
        for folder in sorted(p for p in PLOTS.glob("*/*") if p.is_dir()):
            if f"{folder.parent.name}/{folder.name}" not in written:
                errors.append(f"{folder.relative_to(ROOT)}: графики статьи, которой нет — удалите папку")

    failed = 0
    for article_id, r in reports.items():
        status = "✓" if not r.errors else "✗"
        extra = f", обновлено {r.updated}" if r.updated else ""
        print(f"{status} {article_id} — примеров {r.examples}{extra}")
        for e in r.errors:
            print(f"    {e}")
            github_error(article_id, e)
        failed += bool(r.errors)
    for e in errors:
        print(f"✗ {e}")
        github_error("справочник", e)
    if planned:
        mark = "✗" if strict else "·"
        shown = ", ".join(planned) if strict or len(planned) <= 10 else ", ".join(planned[:5]) + ", …"
        print(f"{mark} В оглавлении, но ещё не написаны ({len(planned)}): {shown}")
    print("─" * 40)
    total = sum(r.examples for r in reports.values())
    print(f"Статей без ошибок: {len(reports) - failed} из {len(reports)} · примеров: {total}")
    if not runnable:
        print("Примеры не выполнялись: версии пакетов не совпадают с requirements-dev.txt.")
    return 1 if failed or errors or (strict and planned) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

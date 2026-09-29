"""Выполнение кода на сайте: Python в браузере (Pyodide в Web Worker).

Модуль загружает src/lib/python/engine.ts — и в браузере, и при проверке в Node.js (scripts/validate_pyodide.ts).
Сообщения странице уходят через функцию post (JSON-строка), результаты — JSON-совместимые.

Задача: код из редактора сохраняется в main.py (номера строк совпадают с редактором, исходник доступен
inspect — на нём работает проверка «решено рекурсивно»), затем выполняется то, что в копируемом файле
идёт после кода решения: tests.py, список _TESTS и runtime/runner.py. Тесты запускает тот же _run_tests.

Пример справочника: runtime/reference_exec.py — тот же запуск, что в валидаторе справочника.

Таймаутов здесь нет — потоков в Pyodide нет. Если ответа нет вовремя, страница завершает воркер.
"""

from __future__ import annotations

import builtins
import io
import json
import os
import shutil
import sys
import tempfile
import time

HOME = os.getcwd()
_post = None
_config: dict = {}
_examples = None  # ExampleRunner — создаётся при первом примере


class InputNotSupported(RuntimeError):
    pass


def _no_input(prompt: object = "") -> str:
    raise InputNotSupported(
        "input() при запуске на сайте не поддерживается: ввода с клавиатуры здесь нет. "
        "Данные передаются в функцию аргументами — в задачах это делают тесты"
    )


def setup(post, config_json: str) -> None:
    """Вызывается один раз после загрузки Pyodide: post — функция отправки сообщения странице."""
    global _post, _config
    _post = post
    _config = json.loads(config_json)
    builtins.input = _no_input
    os.environ["MPLBACKEND"] = "Agg"
    sys.setrecursionlimit(1000)  # как у CPython по умолчанию


def _send(**message) -> None:
    _post(json.dumps(message, ensure_ascii=False))


# ─── Вывод print() ──────────────────────────────────────────────────────────


class _Sink:
    """Собирает stdout и stderr по порядку; сверх лимита отбрасывает. Отправляет порциями не чаще раза в 0,2 с."""

    def __init__(self, max_chars: int, max_lines: int):
        self.max_chars, self.max_lines = max_chars, max_lines
        self.chars = self.lines = 0
        self.truncated = self.truncation_sent = False
        self.pending: list[list[str]] = []
        self.last_flush = time.monotonic()

    def write(self, stream: str, text: str) -> None:
        if self.truncated or not text:
            return
        if self.lines + text.count("\n") > self.max_lines:
            text = "".join(part + "\n" for part in text.split("\n")[: self.max_lines - self.lines])
            self.truncated = True
        if self.chars + len(text) > self.max_chars:
            text = text[: max(0, self.max_chars - self.chars)]
            self.truncated = True
        self.chars += len(text)
        self.lines += text.count("\n")
        if text:
            if self.pending and self.pending[-1][0] == stream:
                self.pending[-1][1] += text
            else:
                self.pending.append([stream, text])
        if self.truncated or time.monotonic() - self.last_flush > 0.2:
            self.flush()

    def flush(self) -> None:
        self.last_flush = time.monotonic()
        if self.pending or (self.truncated and not self.truncation_sent):
            _send(type="output", chunks=self.pending, truncated=self.truncated)
            self.pending = []
            self.truncation_sent = self.truncated


class _Stream(io.TextIOBase):
    def __init__(self, sink: _Sink, name: str):
        self.sink, self.name = sink, name

    @property
    def encoding(self) -> str:
        return "utf-8"

    def writable(self) -> bool:
        return True

    def write(self, text: str) -> int:
        self.sink.write(self.name, str(text))
        return len(text)


def _user_line(error: BaseException, filename: str) -> int | None:
    line = None
    tb = error.__traceback__
    while tb is not None:
        if tb.tb_frame.f_code.co_filename == filename:
            line = tb.tb_lineno
        tb = tb.tb_next
    return line


def _is_memory_error(error_type: str | None, message: str) -> bool:
    return error_type == "MemoryError" or (error_type == "OverflowError" and "памяти" in message)


# ─── Задачи ─────────────────────────────────────────────────────────────────


def run_task(payload_json: str) -> None:
    """payload: code — код из редактора, footer — всё, что в копируемом файле после него (тесты и раннер)."""
    payload = json.loads(payload_json)
    workdir = tempfile.mkdtemp(prefix="run-")
    path = os.path.join(workdir, "main.py")
    with open(path, "w", encoding="utf-8") as f:
        f.write(payload["code"])
    sink = _Sink(_config["maxChars"], _config["maxLines"])
    saved = sys.stdout, sys.stderr
    sys.stdout, sys.stderr = _Stream(sink, "out"), _Stream(sink, "err")
    os.chdir(workdir)
    try:
        done = _run_task(payload, path, sink)
    finally:
        sys.stdout, sys.stderr = saved
        sink.flush()
        os.chdir(HOME)
        shutil.rmtree(workdir, ignore_errors=True)
    _send(type="done", truncated=sink.truncated, **done)


def _run_task(payload: dict, path: str, sink: _Sink) -> dict:
    try:
        code = compile(payload["code"], path, "exec")
    except SyntaxError as e:  # и IndentationError / TabError
        return {"phase": "syntax", "error": {"type": type(e).__name__, "message": e.msg, "line": e.lineno}}
    namespace: dict = {"__name__": "__main__", "__file__": path, "__builtins__": builtins}
    try:
        exec(code, namespace)
    except BaseException as e:  # noqa: BLE001 — ошибка в коде решения вне функций
        message = f"{type(e).__name__}: {e}"
        if isinstance(e, MemoryError) or (isinstance(e, OverflowError) and "index-sized" in str(e)):
            message = f"{type(e).__name__}: не хватило памяти — возможно, создаётся слишком большая структура данных"
        error = {"type": type(e).__name__, "message": message, "line": _user_line(e, path)}
        return {"phase": "load", "error": error, "memory": _is_memory_error(error["type"], message)}

    namespace["__name__"] = "__edu_tests__"  # иначе раннер в конце файла сам запустит тесты с печатью
    exec(compile(payload["footer"], "tests.py", "exec"), namespace)
    tests = [namespace["_test_info"](fn) for fn in namespace["_TESTS"]]
    sink.flush()
    _send(type="tests", tests=tests)

    started = [0.0]

    def on_start(index: int) -> None:
        sink.flush()
        _send(type="test-start", index=index)
        started[0] = time.perf_counter()

    def on_result(index: int, result: dict) -> None:
        elapsed = time.perf_counter() - started[0]
        sink.flush()
        _send(type="test", index=index, result=result, elapsed=round(elapsed, 4))

    results = namespace["_run_tests"](verbose=False, on_start=on_start, on_result=on_result, user_file=path)
    memory = any(_is_memory_error(r["error_type"], r["message"]) for r in results)
    return {"phase": "tests", "results": results, "memory": memory}


# ─── Справочник ─────────────────────────────────────────────────────────────


def run_example(payload_json: str) -> None:
    """payload: setup, code, filename («reference/numpy/broadcasting.py»), cell — id примера."""
    global _examples
    payload = json.loads(payload_json)
    if _examples is None:
        from reference_exec import ExampleRunner

        _examples = ExampleRunner(_config["prelude"], "reference/prelude.py", _config["maxChars"], _config["maxLines"])
    started = time.perf_counter()
    result = _examples.run(payload["setup"], payload["code"], payload["filename"], payload["cell"])
    elapsed = time.perf_counter() - started
    error = result.error
    missing = getattr(error, "name", None) if isinstance(error, ModuleNotFoundError) else None
    _send(
        type="done",
        lines=result.lines,
        error=None if error is None else {"type": type(error).__name__, "mro": [k.__name__ for k in type(error).__mro__], "line": result.error_line},
        missing_module=missing,
        plots=result.plots,
        warnings=sorted({c.__name__ for c in result.categories}),
        truncated=result.truncated,
        elapsed=round(elapsed, 4),
        memory=isinstance(error, MemoryError),
    )

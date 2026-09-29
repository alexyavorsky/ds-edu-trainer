#!/usr/bin/env python3
"""Запускает собранные копируемые файлы и проверяет, что все тесты проходят.

Работает на Python 3.10+ без сторонних модулей (в отличие от validate.py, которому нужен tomllib).
Файлы готовит `python3 scripts/validate.py --export <папка>`.

    python scripts/run_bundles.py <папка>
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

TIMEOUT = 180
SUMMARY = re.compile(r"Прошло (\d+) из (\d+)")


def github_error(title: str, message: str) -> None:
    """В GitHub Actions ошибка видна аннотацией на странице запуска — логи без входа не открываются."""
    if os.environ.get("GITHUB_ACTIONS") == "true":
        esc = lambda s: s.replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")
        print(f"::error title={esc(title).replace(',', '%2C').replace(':', '%3A')}::{esc(message)}")


def check_selfcheck(name: str, proc: subprocess.CompletedProcess) -> str:
    """Синтетические проверки раннера: ожидаемое поведение, а не «все тесты прошли»."""
    out = proc.stdout
    if name == "selfcheck__hang.py":
        ok = "✓ До зависания" in out and "не завершился за 1 с" in out and "– После зависания" in out
        return "" if ok else f"зависший тест обработан неправильно: {out[-300:]!r}"
    if name == "selfcheck__recursion.py":
        return "" if "RecursionError" in out else f"ожидался RecursionError: {out[-300:]!r}"
    if name == "selfcheck__user_test.py":
        return "" if "Прошло 1 из 1" in out else f"функция test_… из решения запустилась как тест: {out[-300:]!r}"
    if name == "selfcheck__deep.py":
        crashed = proc.returncode not in (0, 1) or "Прошло" not in out
        return f"глубокая рекурсия аварийно завершила Python (код {proc.returncode})" if crashed else ""
    return f"неизвестная самопроверка {name}"


def main() -> int:
    folder = Path(sys.argv[1] if len(sys.argv) > 1 else "bundles")
    files = sorted(folder.glob("*.py"))
    if not files:
        print(f"В {folder} нет файлов")
        return 1
    env = {**os.environ, "PYTHONIOENCODING": "utf-8", "PYTHONDONTWRITEBYTECODE": "1"}
    failed = []
    for path in files:
        try:
            proc = subprocess.run(
                [sys.executable, str(path)], capture_output=True, text=True, encoding="utf-8", timeout=TIMEOUT, env=env
            )
        except subprocess.TimeoutExpired:
            failed.append((path.name, f"не завершился за {TIMEOUT} с"))
            continue
        if path.name.startswith("selfcheck__"):
            problem = check_selfcheck(path.name, proc)
            if problem:
                failed.append((path.name, problem))
            continue
        found = SUMMARY.findall(proc.stdout)
        if proc.returncode != 0 or not found or found[-1][0] != found[-1][1]:
            tail = (proc.stdout + proc.stderr).strip().splitlines()[-6:]
            failed.append((path.name, "\n      ".join(tail) or f"код выхода {proc.returncode}"))
    print(f"Python {sys.version.split()[0]} на {sys.platform}: прошли {len(files) - len(failed)} из {len(files)} файлов")
    for name, why in failed:
        print(f"  ✗ {name}\n      {why}")
        github_error(f"{name} · Python {sys.version_info.major}.{sys.version_info.minor} · {sys.platform}", why)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())

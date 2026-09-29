# ─── Запуск тестов ───────────────────────────────────────────────────────────

_TIMEOUT = 2.0  # секунд на тест; отдельный тест может задать свой: test_x.timeout = 10


def _call_with_timeout(target, seconds: float) -> bool:
    """Запускает target() в отдельном потоке. Возвращает False, если за seconds он не завершился."""
    import sys
    import threading

    if sys.platform == "emscripten":  # Python в браузере: потоков нет, таймаут обеспечивает страница
        target()
        return True
    # Большой стек нужен, чтобы глубокая рекурсия давала RecursionError, а не аварийное завершение Python.
    for megabytes in (256, 64, 0):
        try:
            threading.stack_size(megabytes * 1024 * 1024)
            worker = threading.Thread(target=target, daemon=True)
            worker.start()
        except (ValueError, RuntimeError, MemoryError):
            continue
        worker.join(seconds)
        return not worker.is_alive()
    target()  # потоки недоступны — запускаем без таймаута
    return True


def _test_info(fn) -> dict:
    """Описание теста, его лимит времени и сообщение на случай зависания."""
    limit = getattr(fn, "timeout", _TIMEOUT)
    hint = getattr(fn, "timeout_hint", "")
    message = (
        f"тест не завершился за {limit:g} с — возможно, бесконечный цикл или рекурсия: "
        "проверьте, что границы/аргументы изменяются на каждом шаге" + (f". {hint}" if hint else "")
    )
    return {"title": (fn.__doc__ or fn.__name__).strip(), "timeout": limit, "timeout_message": message}


def _error_result(title: str, error: BaseException, user_file: str | None) -> dict:
    """Результат упавшего теста: статус, сообщение, тип исключения и строка в коде решения."""
    line = None
    if user_file:  # самый глубокий кадр в коде решения; ошибка внутри самих тестов — без номера строки
        tb = error.__traceback__
        while tb is not None:
            if tb.tb_frame.f_code.co_filename == user_file:
                line = tb.tb_lineno
            tb = tb.tb_next
    status, message = "error", f"{type(error).__name__}: {error}"
    if isinstance(error, NotImplementedError):
        status, message, line = "not_written", "функция ещё не написана", None
    elif isinstance(error, AssertionError):
        status, message = "failed", str(error) or "проверка не прошла"
    elif isinstance(error, RecursionError):
        message = "RecursionError: слишком глубокая рекурсия — проверьте базовый случай и то, что задача уменьшается"
    elif isinstance(error, MemoryError) or (isinstance(error, OverflowError) and "index-sized" in str(error)):
        message = f"{type(error).__name__}: не хватило памяти — возможно, создаётся слишком большая структура данных"
    return {"title": title, "status": status, "message": message, "error_type": type(error).__name__, "line": line}


def _run_tests(verbose: bool = True, on_start=None, on_result=None, user_file: str | None = None) -> list[dict]:
    """Запускает тесты задачи (_TESTS — функции из tests.py) по порядку, каждый — с таймаутом.

    Возвращает список результатов: {"title", "status", "message", "error_type", "line"}, где status —
    passed · failed · error · not_written · timeout · not_run. Если тест завис, при verbose=True печатает
    итог и завершает процесс: зависший поток остановить нельзя. on_start(i) и on_result(i, результат)
    вызываются по мере выполнения; user_file — имя файла с кодом решения для номеров строк в ошибках.
    """
    import os
    import sys

    if verbose:
        try:  # ✓ и кириллица в консоли Windows со старой кодировкой
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:  # noqa: BLE001 — reconfigure может не быть (перенаправленный вывод, браузер)
            pass

    tests = list(_TESTS)
    results: list[dict] = []
    not_written = hung = False
    for index, fn in enumerate(tests):
        info = _test_info(fn)
        outcome: dict = {}

        def target(fn=fn, outcome=outcome):
            try:
                fn()
            except BaseException as e:
                outcome["error"] = e

        if on_start:
            on_start(index)
        if not _call_with_timeout(target, info["timeout"]):
            results.append({"title": info["title"], "status": "timeout", "message": info["timeout_message"], "error_type": None, "line": None})
            for other in tests[index + 1:]:
                results.append({"title": _test_info(other)["title"], "status": "not_run", "message": "не запускался: предыдущий тест завис", "error_type": None, "line": None})
            hung = True
            break
        error = outcome.get("error")
        if error is None:
            result = {"title": info["title"], "status": "passed", "message": "", "error_type": None, "line": None}
        else:
            result = _error_result(info["title"], error, user_file)
            not_written = not_written or result["status"] == "not_written"
        results.append(result)
        if on_result:
            on_result(index, result)

    if not_written:  # пока функция не написана, «даром» пройденные тесты не засчитываются
        for r in results:
            if r["status"] == "passed":
                r.update(status="not_written", message="не засчитан, пока функция не написана")
    for r in results:
        if len(r["message"]) > 300:
            r["message"] = r["message"][:300] + "…"

    if verbose:
        if not_written:
            print("Функция ещё не написана — замените raise NotImplementedError своим кодом.\n")
        for r in results:
            mark = {"passed": "✓", "not_run": "–"}.get(r["status"], "✗")
            print(f"{mark} {r['title']}")
            if r["message"]:
                print(f"    {r['message']}")
        passed = sum(r["status"] == "passed" for r in results)
        print("─" * 40)
        print(f"Прошло {passed} из {len(results)}" + (" — всё верно!" if passed == len(results) else ""))
        if hung:
            print("Выполнение остановлено: один из тестов завис.")
            sys.stdout.flush()
            os._exit(1)
    return results


if __name__ == "__main__":
    _run_tests()

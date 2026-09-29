# ─── Запуск тестов ───────────────────────────────────────────────────────────

_TIMEOUT = 2.0  # секунд на тест; отдельный тест может задать свой: test_x.timeout = 10


def _call_with_timeout(target, seconds: float) -> bool:
    """Запускает target() в отдельном потоке. Возвращает False, если за seconds он не завершился."""
    import threading

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
    target()  # потоки недоступны (например, Python в браузере) — запускаем без таймаута
    return True


def _run_tests(verbose: bool = True) -> list[tuple[str, bool, str]]:
    """Запускает функции test_* по порядку, каждую — с таймаутом.

    Возвращает список (описание, прошёл ли, сообщение). Если тест завис, при verbose=True
    печатает итог и завершает процесс: зависший поток остановить нельзя.
    """
    import os
    import sys

    tests = [(n, f) for n, f in list(globals().items()) if n.startswith("test_") and callable(f)]
    results: list[tuple[str, bool, str]] = []
    not_written = hung = False
    for index, (name, fn) in enumerate(tests):
        title = (fn.__doc__ or name).strip()
        limit = getattr(fn, "timeout", _TIMEOUT)
        outcome: dict = {}

        def target(fn=fn, outcome=outcome):
            try:
                fn()
            except BaseException as e:
                outcome["error"] = e

        if not _call_with_timeout(target, limit):
            hint = getattr(fn, "timeout_hint", "")
            message = (
                f"тест не завершился за {limit:g} с — возможно, бесконечный цикл или рекурсия: "
                "проверьте, что границы/аргументы изменяются на каждом шаге" + (f". {hint}" if hint else "")
            )
            results.append((title, False, message))
            for other_name, other in tests[index + 1:]:
                results.append(((other.__doc__ or other_name).strip(), False, "не запускался: предыдущий тест завис"))
            hung = True
            break
        error = outcome.get("error")
        if error is None:
            results.append((title, True, ""))
        elif isinstance(error, NotImplementedError):
            not_written = True
            results.append((title, False, "функция ещё не написана"))
        elif isinstance(error, AssertionError):
            results.append((title, False, str(error) or "проверка не прошла"))
        elif isinstance(error, RecursionError):
            results.append((title, False, "RecursionError: слишком глубокая рекурсия — проверьте базовый случай и то, что задача уменьшается"))
        else:
            results.append((title, False, f"{type(error).__name__}: {error}"))

    if not_written:  # пока функция не написана, «даром» пройденные тесты не засчитываются
        results = [(t, False, m or "не засчитан, пока функция не написана") for t, _, m in results]
    results = [(t, ok, m if len(m) <= 300 else m[:300] + "…") for t, ok, m in results]

    if verbose:
        if not_written:
            print("Функция ещё не написана — замените raise NotImplementedError своим кодом.\n")
        for title, ok, message in results:
            mark = "✓" if ok else ("–" if message.startswith("не запускался") else "✗")
            print(f"{mark} {title}")
            if message:
                print(f"    {message}")
        passed = sum(ok for _, ok, _ in results)
        print("─" * 40)
        print(f"Прошло {passed} из {len(results)}" + (" — всё верно!" if passed == len(results) else ""))
        if hung:
            print("Выполнение остановлено: один из тестов завис.")
            sys.stdout.flush()
            os._exit(1)
    return results


if __name__ == "__main__":
    _run_tests()

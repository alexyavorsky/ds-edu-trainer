def find_files(folder: dict, ext: str) -> list[str]:
    """Возвращает пути всех файлов с расширением ext внутри folder."""
    result: list[str] = []
    _walk(folder, "", ext, result)
    return result


def _walk(folder: dict, prefix: str, ext: str, result: list[str]) -> None:
    """Обходит папку, дописывая подходящие пути в result."""
    for name, item in folder.items():
        path = prefix + name
        if isinstance(item, dict):
            # TODO: рекурсивный случай — обойдите подпапку.
            #       Какой префикс будет у путей внутри неё?
            pass
        elif name.endswith(ext):
            # TODO: базовый случай — файл подходит
            pass

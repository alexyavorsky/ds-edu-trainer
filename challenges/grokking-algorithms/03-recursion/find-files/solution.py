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
            _walk(item, path + "/", ext, result)
        elif name.endswith(ext):
            result.append(path)

def common_motif_length(a: str, b: str) -> int:
    """Длина самой длинной общей подпоследовательности строк a и b."""
    table = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            if a[i - 1] == b[j - 1]:
                # TODO: ноты совпали
                pass
            else:
                # TODO: ноты не совпали
                pass
    return table[len(a)][len(b)]

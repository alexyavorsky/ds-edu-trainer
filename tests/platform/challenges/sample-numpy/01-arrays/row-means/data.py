import random

import numpy as np


def sample_scores(rows: int = 4, seed: int = 7) -> np.ndarray:
    """Оценки от 2 до 5: rows учеников × 3 предмета, воспроизводимо при одном seed."""
    rng = random.Random(seed)
    return np.array([[rng.randint(2, 5) for _ in range(3)] for _ in range(rows)])

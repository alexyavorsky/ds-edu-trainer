import numpy as np


def row_means(scores: np.ndarray) -> np.ndarray:
    return np.asarray(scores).mean(axis=1)

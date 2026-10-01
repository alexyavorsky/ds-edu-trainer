def test_small():
    """[[2, 4], [3, 5]] → [3.0, 4.0]"""
    assert np.allclose(row_means(np.array([[2, 4], [3, 5]])), [3.0, 4.0])


def test_shape():
    """Для sample_scores(): по одному среднему на строку"""
    assert np.shape(row_means(sample_scores())) == (4,)


def test_values():
    """Средние совпадают с посчитанными вручную"""
    data = sample_scores(rows=3, seed=1)
    expected = [sum(row) / len(row) for row in data.tolist()]
    assert np.allclose(row_means(data), expected)

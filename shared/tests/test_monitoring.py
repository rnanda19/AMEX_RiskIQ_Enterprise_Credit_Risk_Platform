import numpy as np

from shared.monitoring import psi_bin_share


def test_returns_none_below_three_edges():
    assert psi_bin_share([0, 1], np.array([0.5, 0.5])) is None


def test_bin_share_sums_to_approximately_one():
    rng = np.random.default_rng(3)
    edges = [0.0, 0.25, 0.5, 0.75, 1.0]
    window = rng.random(1000)
    shares = psi_bin_share(edges, window)
    assert shares is not None
    assert len(shares) == 4  # 4 bins from 5 edges
    assert sum(shares) == pytest_approx_one()


def pytest_approx_one():
    import pytest
    return pytest.approx(1.0, abs=1e-3)


def test_empty_window_does_not_crash():
    edges = [0.0, 0.5, 1.0]
    shares = psi_bin_share(edges, np.array([]))
    assert shares is not None
    # clipped to a floor of 1e-6 per bin, not zero-division
    assert all(s > 0 for s in shares)

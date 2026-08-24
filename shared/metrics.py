"""Official AMEX competition metric -- extracted verbatim (same algorithm,
same code) from Problem1_Credit_Scoring_PD_Prediction/notebooks/
05_model_development.ipynb, Section 3.

This is the single source of truth for the metric going forward. The
notebook keeps its own inline copy for now (see shared/__init__.py for why),
but any NEW notebook, service, or test in this platform should import from
here rather than re-typing the algorithm again.
"""
from __future__ import annotations

import numpy as np


def amex_metric_numpy(y_true: "np.ndarray", y_pred: "np.ndarray") -> float:
    """Official American Express - Default Prediction competition metric:
    0.5 * (Normalized Weighted Gini) + 0.5 * (Top-4% Capture Rate).

    Non-defaulters (target=0) are weighted 20x relative to defaulters
    (target=1) in both sub-metrics -- this reflects the competition's
    real-world cost asymmetry between the two classes. This is a
    vectorized numpy equivalent of the official pandas reference
    implementation published by the competition host.
    """
    y_true = np.asarray(y_true, dtype=np.float64)
    y_pred = np.asarray(y_pred, dtype=np.float64)

    def top_four_percent_captured(yt, yp):
        order = np.argsort(-yp, kind="mergesort")
        yt_sorted = yt[order]
        weight = np.where(yt_sorted == 0, 20.0, 1.0)
        cum_weight = np.cumsum(weight)
        cutoff = 0.04 * weight.sum()
        mask = cum_weight <= cutoff
        total_pos = yt_sorted.sum()
        if total_pos == 0:
            return 0.0
        return float(yt_sorted[mask].sum() / total_pos)

    def weighted_gini(yt, yp):
        order = np.argsort(-yp, kind="mergesort")
        yt_sorted = yt[order]
        weight = np.where(yt_sorted == 0, 20.0, 1.0)
        random_cum = np.cumsum(weight / weight.sum())
        total_pos_weighted = (yt_sorted * weight).sum()
        if total_pos_weighted == 0:
            return 0.0
        cum_pos_found = np.cumsum(yt_sorted * weight)
        lorentz = cum_pos_found / total_pos_weighted
        return float(((lorentz - random_cum) * weight).sum())

    g_actual = weighted_gini(y_true, y_pred)
    g_perfect = weighted_gini(y_true, y_true)
    normalized_gini = g_actual / g_perfect if g_perfect != 0 else 0.0
    top4 = top_four_percent_captured(y_true, y_pred)
    return 0.5 * (normalized_gini + top4)


def top_four_percent_capture_only(y_true, y_pred) -> float:
    """Standalone top-4% capture rate (reported separately in the comparison
    table, in addition to being one half of amex_metric_numpy)."""
    y_true = np.asarray(y_true, dtype=np.float64)
    y_pred = np.asarray(y_pred, dtype=np.float64)
    order = np.argsort(-y_pred, kind="mergesort")
    yt_sorted = y_true[order]
    weight = np.where(yt_sorted == 0, 20.0, 1.0)
    cum_weight = np.cumsum(weight)
    cutoff = 0.04 * weight.sum()
    mask = cum_weight <= cutoff
    total_pos = yt_sorted.sum()
    if total_pos == 0:
        return 0.0
    return float(yt_sorted[mask].sum() / total_pos)

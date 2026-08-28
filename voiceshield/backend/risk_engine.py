from __future__ import annotations

import numpy as np


def aggregate_risk(spoof_scores: list[float], quality_score: float, dispersion: float) -> dict:
    """Turn window-level AASIST scores into an interpretable policy score.

    This is deliberately a policy score, not a calibrated probability. The UI
    should use the review band to avoid presenting borderline model outputs as
    certain decisions.
    """
    if not spoof_scores:
        raise ValueError("No window scores supplied")

    arr = np.asarray(spoof_scores, dtype=np.float32)
    mean_score = float(arr.mean())
    median_score = float(np.median(arr))
    peak_score = float(arr.max())
    high_ratio = float(np.mean(arr >= 0.70))
    very_high_ratio = float(np.mean(arr >= 0.85))

    # Persistence matters more than a single extreme window.
    evidence = (
        0.45 * mean_score
        + 0.25 * median_score
        + 0.20 * high_ratio
        + 0.10 * peak_score
    )

    # A small quality penalty prevents bad recordings from looking more
    # trustworthy than they are; it does not convert quality into a label.
    quality_factor = 1.0 if quality_score >= 80 else 0.94 if quality_score >= 60 else 0.86
    risk = float(np.clip(100.0 * evidence * quality_factor, 0, 100))

    if risk >= 72:
        level = "HIGH"
        action = "SECONDARY VERIFICATION"
    elif risk >= 43:
        level = "MEDIUM"
        action = "REVIEW / VERIFY"
    else:
        level = "LOW"
        action = "ALLOW WITH MONITORING"

    # Scores close to the decision boundary should be presented as uncertain.
    review_band = 38 <= risk <= 60
    if review_band:
        confidence = "BORDERLINE"
    elif risk >= 72 or risk <= 25:
        confidence = "STRONGER"
    else:
        confidence = "MODERATE"

    return {
        "risk_score": round(risk, 2),
        "risk_level": level,
        "recommended_action": action,
        "confidence_band": confidence,
        "needs_review": review_band,
        "mean_spoof_score": round(mean_score * 100, 2),
        "median_spoof_score": round(median_score * 100, 2),
        "peak_spoof_score": round(peak_score * 100, 2),
        "high_risk_window_ratio": round(high_ratio * 100, 2),
        "very_high_risk_window_ratio": round(very_high_ratio * 100, 2),
        "window_score_dispersion": round(float(dispersion) * 100, 2),
    }

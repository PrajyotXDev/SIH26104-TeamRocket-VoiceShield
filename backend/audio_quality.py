from __future__ import annotations

import numpy as np

from .preprocessing import AudioInfo


def assess_audio_quality(audio: np.ndarray, info: AudioInfo) -> dict:
    rms_db = float(20.0 * np.log10(max(info.rms, 1e-7)))
    peak_db = float(20.0 * np.log10(max(info.peak, 1e-7)))
    dynamic_range = float(max(peak_db - rms_db, 0.0))

    issues: list[str] = []
    if info.duration_seconds < 2.0:
        issues.append("Very short recording")
    if rms_db < -45:
        issues.append("Low signal level")
    if info.clipped:
        issues.append("Possible clipping")

    score = 100.0
    score -= min(35.0, max(0.0, -35.0 - rms_db))
    score -= 15.0 if info.clipped else 0.0
    score -= 15.0 if info.duration_seconds < 2.0 else 0.0
    score = float(np.clip(score, 0, 100))

    quality = "GOOD" if score >= 80 else "FAIR" if score >= 60 else "POOR"
    return {
        "quality_score": round(score, 2),
        "quality_label": quality,
        "rms_db": round(rms_db, 2),
        "peak_db": round(peak_db, 2),
        "dynamic_range_db": round(dynamic_range, 2),
        "issues": issues,
    }

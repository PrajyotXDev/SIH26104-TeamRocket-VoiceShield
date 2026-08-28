from __future__ import annotations


def build_indicators(window_results: list[dict], quality: dict) -> list[dict]:
    """Return human-readable, model-derived evidence indicators.

    These are observations about model scores and recording quality. They are
    intentionally not framed as causal explanations for why AASIST decided.
    """
    indicators: list[dict] = []
    scores = [float(r["spoof_score"]) for r in window_results]
    if not scores:
        return indicators

    high = [i for i, s in enumerate(scores) if s >= 0.70]
    very_high = [i for i, s in enumerate(scores) if s >= 0.85]
    if very_high:
        indicators.append({"severity": "high", "title": "Strong spoof-model evidence", "detail": f"{len(very_high)} segment(s) crossed the 85% model-score mark."})
    if len(high) >= max(1, len(scores) // 3):
        indicators.append({"severity": "high", "title": "Persistent suspicious evidence", "detail": f"{len(high)} of {len(scores)} segments crossed the 70% model-score mark."})
    spread = max(scores) - min(scores)
    if len(scores) > 1 and spread > 0.45:
        indicators.append({"severity": "medium", "title": "High temporal variation", "detail": "Model scores change substantially across the recording; inspect the highlighted timeline."})
    if quality.get("issues"):
        for issue in quality["issues"]:
            indicators.append({"severity": "medium", "title": "Recording-quality caveat", "detail": issue})
    if not indicators:
        indicators.append({"severity": "low", "title": "No strong risk pattern detected", "detail": "No segment crossed the configured high-risk evidence thresholds."})
    return indicators

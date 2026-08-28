from backend.explainability import build_indicators


def test_explainability_returns_structured_indicators():
    rows = [
        {"spoof_score": 0.91},
        {"spoof_score": 0.86},
        {"spoof_score": 0.20},
    ]
    out = build_indicators(rows, {"issues": []})
    assert out
    assert all("title" in item and "detail" in item for item in out)

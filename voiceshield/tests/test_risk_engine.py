from backend.risk_engine import aggregate_risk


def test_low_risk():
    r = aggregate_risk([0.1, 0.2, 0.15], 100, 0.05)
    assert r["risk_level"] == "LOW"
    assert r["needs_review"] is False


def test_persistent_high_risk():
    r = aggregate_risk([0.9, 0.85, 0.8, 0.88], 100, 0.04)
    assert r["risk_level"] == "HIGH"
    assert r["high_risk_window_ratio"] == 100.0


def test_borderline_is_flagged_for_review():
    r = aggregate_risk([0.55, 0.55, 0.55], 100, 0.0)
    assert r["needs_review"] is True

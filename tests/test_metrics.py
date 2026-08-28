from evaluation.metrics import binary_metrics


def test_metrics_basic():
    metrics = binary_metrics([0, 1, 1, 0], [0.1, 0.9, 0.8, 0.2])
    assert metrics["accuracy"] == 1.0
    assert metrics["f1"] == 1.0

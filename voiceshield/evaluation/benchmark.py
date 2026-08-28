from __future__ import annotations

import argparse
import csv
import json
import time
from pathlib import Path

from backend.detector import Detector
from .metrics import binary_metrics


def main():
    ap = argparse.ArgumentParser(description="Evaluate detector using a CSV manifest")
    ap.add_argument("manifest", help="CSV with path,label where label is 0=bonafide, 1=spoof")
    ap.add_argument("--output", default="evaluation/results.json")
    args = ap.parse_args()

    detector = Detector()
    y_true, scores = [], []
    rows = []
    with open(args.manifest, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            t0 = time.perf_counter()
            result = detector.analyze(row["path"])
            elapsed = time.perf_counter() - t0
            y_true.append(int(row["label"]))
            score = result["risk"]["mean_spoof_score"] / 100.0
            scores.append(score)
            rows.append({"path": row["path"], "label": row["label"], "score": score, "latency_s": elapsed})

    result = {"metrics": binary_metrics(y_true, scores), "samples": rows}
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result["metrics"], indent=2))


if __name__ == "__main__":
    main()

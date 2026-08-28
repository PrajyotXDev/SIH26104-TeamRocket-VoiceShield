from __future__ import annotations

import time
from pathlib import Path

import numpy as np

from .audio_quality import assess_audio_quality
from .explainability import build_indicators
from .model import AASISTModel
from .preprocessing import load_audio, make_windows
from .risk_engine import aggregate_risk


class Detector:
    def __init__(self):
        self.model = AASISTModel()

    def analyze(self, audio_path: str | Path, hop_seconds: float = 2.0) -> dict:
        t0 = time.perf_counter()
        audio, info = load_audio(audio_path)
        quality = assess_audio_quality(audio, info)
        windows = make_windows(audio, hop_seconds=hop_seconds)

        batch = np.stack([w for _, w in windows], axis=0)
        inference_t0 = time.perf_counter()
        probs = self.model.predict_batch(batch)
        inference_ms = (time.perf_counter() - inference_t0) * 1000

        results = []
        for idx, ((start, _), p) in enumerate(zip(windows, probs)):
            # AASIST checkpoints used by VoiceShield follow the ASVspoof
            # convention used by this project: class 0 = bonafide,
            # class 1 = spoof.  Keep this mapping explicit because swapping
            # these two probabilities inverts the complete risk assessment.
            bonafide = float(p[0])
            spoof = float(p[1])
            results.append({
                "index": idx,
                "start_seconds": round(start, 2),
                "end_seconds": round(start + 4.0375, 2),
                "bonafide_score": round(bonafide, 6),
                "spoof_score": round(spoof, 6),
                "label": "SPOOF" if spoof >= bonafide else "BONAFIDE",
            })

        spoof_scores = [r["spoof_score"] for r in results]
        dispersion = float(np.std(spoof_scores)) if len(spoof_scores) > 1 else 0.0
        risk = aggregate_risk(spoof_scores, quality["quality_score"], dispersion)
        indicators = build_indicators(results, quality)

        elapsed_ms = (time.perf_counter() - t0) * 1000
        return {
            "model": "AASIST",
            "device": self.model.device_name,
            "verdict": "SPOOF" if risk["risk_score"] >= 50 else "BONAFIDE",
            "risk": risk,
            "audio": {
                "duration_seconds": round(info.duration_seconds, 3),
                "original_sample_rate": info.original_sample_rate,
                "channels": info.channels,
                "resampled_to": 16000,
            },
            "quality": quality,
            "windows_analyzed": len(results),
            "windows": results,
            "indicators": indicators,
            "decision": {
                "needs_review": bool(risk.get("needs_review", False)),
                "confidence_band": risk.get("confidence_band", "MODERATE"),
                "note": "Risk is a policy score built from AASIST window scores; it is not a calibrated probability.",
            },
            "performance": {
                "inference_ms": round(inference_ms, 2),
                "total_ms": round(elapsed_ms, 2),
                "windows_per_second": round(len(results) / max(elapsed_ms / 1000, 1e-6), 2),
            },
        }

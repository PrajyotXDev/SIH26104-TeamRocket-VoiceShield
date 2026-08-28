from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import soundfile as sf

try:
    import scipy.signal as sps
except ImportError as exc:  # pragma: no cover
    sps = None
    _SCIPY_IMPORT_ERROR = exc
else:
    _SCIPY_IMPORT_ERROR = None

from .config import TARGET_SR, WINDOW_SAMPLES


@dataclass
class AudioInfo:
    path: str
    original_sample_rate: int
    duration_seconds: float
    channels: int
    peak: float
    rms: float
    clipped: bool
    resampled: bool


def load_audio(path: str | Path, target_sr: int = TARGET_SR) -> tuple[np.ndarray, AudioInfo]:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Audio file not found: {p}")

    audio, sr = sf.read(str(p), always_2d=False)
    channels = 1 if audio.ndim == 1 else int(audio.shape[1])
    if audio.ndim > 1:
        audio = np.mean(audio, axis=1)
    audio = np.asarray(audio, dtype=np.float32)

    if audio.size == 0:
        raise ValueError("Audio file contains no samples.")

    original_sr = int(sr)
    resampled = original_sr != target_sr
    if resampled:
        if sps is None:
            raise RuntimeError("scipy is required for high-quality resampling") from _SCIPY_IMPORT_ERROR
        gcd = np.gcd(original_sr, target_sr)
        up = target_sr // gcd
        down = original_sr // gcd
        audio = sps.resample_poly(audio, up, down).astype(np.float32)

    peak = float(np.max(np.abs(audio)))
    rms = float(np.sqrt(np.mean(np.square(audio)) + 1e-12))
    duration = float(len(audio) / target_sr)
    clipped = bool(np.mean(np.abs(audio) >= 0.999) > 0.001)

    info = AudioInfo(
        path=str(p),
        original_sample_rate=original_sr,
        duration_seconds=duration,
        channels=channels,
        peak=peak,
        rms=rms,
        clipped=clipped,
        resampled=resampled,
    )
    return audio, info


def normalize_audio(audio: np.ndarray) -> np.ndarray:
    audio = np.asarray(audio, dtype=np.float32)
    max_abs = float(np.max(np.abs(audio)))
    if max_abs > 1.0:
        audio = audio / max_abs
    return np.nan_to_num(audio).astype(np.float32)


def make_windows(
    audio: np.ndarray,
    window_samples: int = WINDOW_SAMPLES,
    hop_seconds: float = 2.0,
    sr: int = TARGET_SR,
) -> list[tuple[float, np.ndarray]]:
    audio = normalize_audio(audio)
    if len(audio) == 0:
        raise ValueError("No audio samples available")

    hop = max(1, int(round(hop_seconds * sr)))
    if len(audio) <= window_samples:
        padded = np.tile(audio, int(np.ceil(window_samples / len(audio))))[:window_samples]
        return [(0.0, padded)]

    starts = list(range(0, len(audio) - window_samples + 1, hop))
    final_start = len(audio) - window_samples
    if starts[-1] != final_start:
        starts.append(final_start)

    windows = []
    for start in starts:
        windows.append((start / sr, audio[start:start + window_samples]))
    return windows

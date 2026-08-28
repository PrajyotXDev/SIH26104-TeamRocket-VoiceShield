import numpy as np
from backend.preprocessing import make_windows


def test_short_audio_is_padded():
    audio = np.zeros(16000, dtype=np.float32)
    windows = make_windows(audio)
    assert len(windows) == 1
    assert len(windows[0][1]) == 64600


def test_long_audio_has_multiple_windows():
    audio = np.zeros(16000 * 10, dtype=np.float32)
    windows = make_windows(audio, hop_seconds=2)
    assert len(windows) > 1

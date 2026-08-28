from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "config" / "AASIST.conf"
MODEL_PATH = ROOT / "models" / "weights" / "AASIST.pth"
TARGET_SR = 16000
WINDOW_SAMPLES = 64600
WINDOW_SECONDS = WINDOW_SAMPLES / TARGET_SR
DEFAULT_HOP_SECONDS = 2.0

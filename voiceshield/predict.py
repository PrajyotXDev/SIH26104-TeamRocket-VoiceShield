"""Original single-window AASIST CLI kept for backward compatibility.

For the hackathon demo, prefer `python scripts/run_detector.py <audio>` because
it uses the new multi-window VoiceShield pipeline.
"""
import json
import sys
from pathlib import Path

import numpy as np
import soundfile as sf
import torch
import torch.nn.functional as F

from models.AASIST import Model

BASE_DIR = Path(__file__).resolve().parent
CONFIG_PATH = BASE_DIR / "config" / "AASIST.conf"
MODEL_PATH = BASE_DIR / "models" / "weights" / "AASIST.pth"
TARGET_LENGTH = 64600

with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    config = json.load(f)

model_config = config["model_config"]
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Device: {device}")
if device.type == "cuda":
    print(f"GPU: {torch.cuda.get_device_name(0)}")

print("Loading AASIST model...")
model = Model(model_config)
model.load_state_dict(torch.load(MODEL_PATH, map_location=device, weights_only=True))
model.to(device)
model.eval()
print("Model loaded successfully.")


def prepare_audio(audio_path):
    audio, sample_rate = sf.read(audio_path)
    if audio.ndim > 1:
        audio = np.mean(audio, axis=1)
    audio = audio.astype(np.float32)
    if sample_rate != 16000:
        audio_tensor = torch.tensor(audio, dtype=torch.float32).unsqueeze(0).unsqueeze(0)
        new_length = int(len(audio) * 16000 / sample_rate)
        audio = F.interpolate(audio_tensor, size=new_length, mode="linear", align_corners=False).squeeze().numpy()
    if len(audio) >= TARGET_LENGTH:
        audio = audio[:TARGET_LENGTH]
    else:
        audio = np.tile(audio, int(np.ceil(TARGET_LENGTH / len(audio))))[:TARGET_LENGTH]
    return torch.tensor(audio, dtype=torch.float32)


def predict(audio_path):
    audio = prepare_audio(audio_path).unsqueeze(0).to(device)
    with torch.inference_mode():
        _, logits = model(audio)
        probabilities = torch.softmax(logits, dim=1)
    probs = probabilities[0].cpu().numpy()
    prediction = int(torch.argmax(probabilities, dim=1).item())
    label = "BONAFIDE" if prediction == 1 else "SPOOF"
    return label, probs


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python predict.py <audio_file.wav>")
        sys.exit(1)
    audio_file = sys.argv[1]
    if not Path(audio_file).exists():
        print(f"File not found: {audio_file}")
        sys.exit(1)
    label, probabilities = predict(audio_file)
    print("\n" + "=" * 50)
    print("AASIST AUDIO SPOOF DETECTOR")
    print("=" * 50)
    print(f"Prediction: {label}")
    print(f"Bonafide probability: {probabilities[1] * 100:.2f}%")
    print(f"Spoof probability:    {probabilities[0] * 100:.2f}%")
    print("=" * 50)

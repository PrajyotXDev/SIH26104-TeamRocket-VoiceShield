# VoiceShield — Deepfake Voice Forensics

VoiceShield is a hackathon-oriented layer around the AASIST anti-spoofing model. It turns a single model score into a product-style workflow: audio quality checks, overlapping segment analysis, evidence indicators, risk aggregation, a browser UI, and a local API.

## Architecture

```text
audio upload / microphone
        ↓
 decode + mono + 16 kHz
        ↓
 recording quality checks
        ↓
 overlapping ~4 s windows
        ↓
 AASIST inference (GPU/CPU)
        ↓
 per-window spoof evidence
        ↓
 risk policy + review band
        ↓
 timeline + evidence + action
```

## Quick start (Windows)

1. Activate the existing virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

2. Install application dependencies:

```powershell
pip install -r requirements_app.txt
```

3. Start the complete app:

```powershell
python -m uvicorn api_server:app --host 127.0.0.1 --port 8000
```

4. Open **http://127.0.0.1:8000**.

You can also run `run_app.bat` on Windows.

## CLI

```powershell
python scripts/run_detector.py test.wav
python scripts/run_detector.py test.wav --hop 1.0
```

The original `predict.py` is preserved for backward compatibility. The new multi-window detector is the recommended demo path.

## API

- `GET /health`
- `POST /predict` with multipart field `file`
- `GET /` serves the new frontend

Maximum upload size: 50 MB.

## Evaluation

Create `evaluation/manifest.csv`:

```csv
path,label
/path/to/genuine.wav,0
/path/to/spoof.wav,1
```

Run:

```powershell
python -m evaluation.benchmark evaluation/manifest.csv
```

## What makes the demo stronger

### 1. Segment-level evidence

Long recordings are split into overlapping windows, so a single early or late segment does not dominate the entire decision.

### 2. Review band

Borderline results are marked for review rather than being presented as certain. The risk number is a policy score, not a calibrated probability.

### 3. Audio quality

Signal level, clipping, dynamic range and duration are surfaced separately. Poor quality reduces confidence in the risk policy rather than being treated as evidence of spoofing.

### 4. Interactive forensics timeline

The frontend highlights suspicious windows and lets the presenter inspect each window's spoof and bonafide model scores.

## Important scientific limitation

AASIST was trained for anti-spoofing benchmarks and its raw softmax scores should not be described as calibrated real-world probabilities without validation. Before claiming accuracy, benchmark on representative genuine and spoof data, ideally with speaker-disjoint evaluation and a held-out test set.

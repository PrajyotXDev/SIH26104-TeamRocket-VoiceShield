<div align="center">

# 🛡️ VoiceShield
### AI-Powered Voice Authenticity & Deepfake Detection

**Detect • Explain • Quantify**

AASIST-powered multi-window voice anti-spoofing with temporal evidence, audio-quality assessment, and an interactive forensic-style dashboard.

[![Smart India Hackathon](https://img.shields.io/badge/Smart%20India%20Hackathon-2026-ff7a00?style=for-the-badge)](https://www.sih.gov.in/)
[![Problem Statement](https://img.shields.io/badge/SIH-SIH26104-7c5cff?style=for-the-badge)](https://www.sih.gov.in/)
[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-Deep%20Learning-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)](https://pytorch.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)

**TeamRocket • Smart India Hackathon 2026**

</div>

---

## 🎯 The Problem

Voice cloning has made convincing impersonation attacks increasingly practical. A malicious recording can be used in financial fraud, identity impersonation, social engineering, authentication attacks, and misleading digital-media content.

The usual experience is a single opaque answer:

> **“Real” or “Fake.”**

That is not enough for a security workflow. A useful system should help answer three questions:

**Is it suspicious?**  
**Where is the suspicious evidence?**  
**Why did the system reach that decision?**

---

## 💡 Our Solution

**VoiceShield** turns voice spoof detection into an evidence-driven analysis pipeline.

```text
Audio
  │
  ▼
Validation + Preprocessing
  │
  ▼
Overlapping ~4s Windows
  │
  ▼
AASIST Anti-Spoofing Model
  │
  ├───────────────┐
  ▼               ▼
Window Scores   Audio Quality
  │               │
  └───────┬───────┘
          ▼
   Temporal Evidence
          │
          ▼
      Risk Engine
          │
          ▼
   Explainability Layer
          │
          ▼
   Interactive Dashboard
```

Instead of collapsing an entire recording into one black-box prediction, VoiceShield analyzes overlapping windows and exposes the evidence behind the final risk assessment.

---

## ⭐ Why VoiceShield Stands Out

### 1. Window-level intelligence
A recording can contain changing model behaviour. VoiceShield shows **which time regions are suspicious** rather than only returning a recording-level label.

### 2. Evidence, not just a verdict
The dashboard surfaces indicators such as **strong spoof-model evidence**, **persistent suspicious evidence**, and **high temporal variation**.

### 3. Risk is separated from raw model output
The application distinguishes AASIST model evidence from its application-level **policy risk score**. The risk score is **not presented as a calibrated probability**.

### 4. Quality-aware analysis
Recording characteristics are evaluated separately so users can see when audio quality may affect confidence.

### 5. Judge-friendly interactive demo
Upload audio, compare results, inspect the timeline, and see the evidence update in a live dashboard.

---

## 🚀 Key Features

| Feature | What it does |
|---|---|
| 🎙️ Audio upload | Analyze WAV, FLAC, OGG, and MP3 recordings |
| 🧠 AASIST inference | Anti-spoofing model for speech authenticity analysis |
| 🪟 Multi-window analysis | Evaluates overlapping time segments |
| 📊 Risk engine | Aggregates window-level evidence into a policy risk score |
| 🔍 Explainability | Converts model behaviour into readable evidence indicators |
| 🎧 Audio-quality panel | Exposes recording characteristics and quality information |
| 📈 Suspicion timeline | Visualizes suspicious windows across the recording |
| ⚡ Performance metrics | Reports inference time, total processing time, and throughput |
| 🌐 Web dashboard | Interactive browser-based interface |
| 🧪 CLI mode | Run the detector directly from the terminal |

---

## 🖥️ Product Flow

```text
1. Upload / record audio
            ↓
2. Normalize + resample
            ↓
3. Split into overlapping windows
            ↓
4. Run AASIST inference
            ↓
5. Compare BONAFIDE vs SPOOF evidence
            ↓
6. Aggregate temporal risk
            ↓
7. Explain the result
            ↓
8. Inspect the timeline in the UI
```

---

## 🧩 System Architecture

```text
                    ┌──────────────────────┐
                    │      Web Browser     │
                    │   VoiceShield UI     │
                    └──────────┬───────────┘
                               │
                               │ POST /predict
                               ▼
                    ┌──────────────────────┐
                    │       FastAPI        │
                    │      api_server     │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │       Detector       │
                    └──────────┬───────────┘
                               │
          ┌────────────────────┼────────────────────┐
          ▼                    ▼                    ▼
 ┌────────────────┐   ┌────────────────┐   ┌────────────────┐
 │ Preprocessing  │   │ Audio Quality  │   │ AASIST Model   │
 └────────────────┘   └────────────────┘   └────────────────┘
          │                    │                    │
          └────────────────────┼────────────────────┘
                               ▼
                    ┌──────────────────────┐
                    │ Temporal / Windows  │
                    └──────────┬───────────┘
                               ▼
                    ┌──────────────────────┐
                    │     Risk Engine      │
                    └──────────┬───────────┘
                               ▼
                    ┌──────────────────────┐
                    │   Explainability     │
                    └──────────┬───────────┘
                               ▼
                    ┌──────────────────────┐
                    │ JSON → Dashboard     │
                    └──────────────────────┘
```

---

## 📁 Project Structure

```text
SIH26104-TeamRocket-VoiceShield/
│
├── backend/
│   ├── detector.py            # End-to-end detection pipeline
│   ├── preprocessing.py       # Audio loading / resampling / windows
│   ├── model.py               # AASIST model interface
│   ├── audio_quality.py       # Recording-quality assessment
│   ├── explainability.py      # Human-readable indicators
│   ├── risk_engine.py         # Policy risk aggregation
│   └── config.py              # Backend configuration
│
├── frontend/
│   ├── index.html              # Dashboard UI
│   ├── app.js                  # Frontend logic / API integration
│   └── styles.css              # Dashboard styling
│
├── models/                     # Model implementation / weights
├── config/                     # Model and application configuration
├── scripts/                    # CLI and helper scripts
├── tests/                      # Automated tests
├── evaluation/                 # Evaluation utilities
├── analysis/                   # Analysis artifacts / experiments
│
├── api_server.py               # FastAPI application
├── predict.py                  # Direct prediction entry point
├── requirements.txt            # Python dependencies
├── LICENSE
└── README.md
```

---

## ⚙️ Technology Stack

**AI / ML**
- AASIST
- PyTorch
- NumPy

**Backend**
- Python
- FastAPI
- Uvicorn

**Audio**
- SoundFile
- SciPy / resampling pipeline

**Frontend**
- HTML
- CSS
- Vanilla JavaScript

**Development**
- Git
- GitHub
- Visual Studio Code

---

## 🛠️ Installation

### 1. Clone

```bash
git clone https://github.com/PrajyotXDev/SIH26104-TeamRocket-VoiceShield.git
cd SIH26104-TeamRocket-VoiceShield
```

### 2. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

The API expects multipart form-data support. If it is not already installed:

```powershell
python -m pip install python-multipart
```

---

## ▶️ Run the Web App

From the repository root:

```powershell
python -m uvicorn api_server:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

Health check:

```text
http://127.0.0.1:8000/health
```

---

## 🧪 Run from the Terminal

You can test the detector without the web UI:

```powershell
python -m scripts.run_detector myvoice.wav
```

The result contains model/device information, verdict, risk, audio metadata, quality information, window-level scores, explainability indicators, decision information, and performance metrics.

---

## 📡 API

### `GET /health`

Returns service health, model information, device information, and version information.

### `POST /predict`

Accepts an uploaded audio file and returns the VoiceShield analysis.

Example high-level response shape:

```json
{
  "model": "AASIST",
  "device": "...",
  "verdict": "BONAFIDE",
  "risk": {
    "risk_score": 10,
    "risk_level": "LOW"
  },
  "windows_analyzed": 7,
  "windows": [],
  "indicators": [],
  "decision": {},
  "performance": {}
}
```

> The exact values depend on the submitted audio and local inference environment.

---

## 🔬 How Multi-Window Analysis Works

For a typical recording, VoiceShield analyzes overlapping windows such as:

```text
00:00 ───── 04:04  → BONAFIDE
02:00 ───── 06:04  → BONAFIDE
04:00 ───── 08:04  → SPOOF
06:00 ───── 10:04  → SPOOF
08:00 ───── 12:04  → SPOOF
```

This makes temporal behaviour visible and helps the user focus attention on suspicious regions.

---

## 🔎 Explainability

VoiceShield can surface evidence such as:

**Strong spoof-model evidence**  
Several windows cross a high spoof-score threshold.

**Persistent suspicious evidence**  
Suspicious evidence appears throughout a significant portion of the recording.

**High temporal variation**  
Model scores change substantially across the recording, encouraging timeline inspection.

The objective is to move from **prediction → evidence → human verification**.

---

## 🎬 Recommended SIH Demo

For a strong live demo:

1. Open the dashboard.
2. Show the API status and active device.
3. Upload a genuine recording.
4. Show the low-risk / bonafide result.
5. Upload a spoof or synthetic sample.
6. Show the risk and verdict change.
7. Open the window-level timeline.
8. Point out suspicious time regions.
9. Show the explainability indicators.
10. Explain that the risk score is a policy score, not a calibrated probability.
11. Optionally demonstrate CLI inference in the terminal.

### Suggested judge narrative

> “Most detectors stop at ‘fake’ or ‘real’. VoiceShield adds the missing evidence layer: it analyzes overlapping segments, measures persistent spoof evidence, factors recording quality, and shows where and why the recording became suspicious.”

---

## 🔐 Privacy & Security Positioning

The current API processes uploaded files temporarily for inference and removes the temporary file after processing.

For a production deployment, add:

- Authentication
- HTTPS
- Rate limiting
- Access control
- Encryption
- Secure logging
- Data-retention policy
- User consent/privacy controls

---

## ⚠️ Limitations

VoiceShield is a research / hackathon prototype.

- Model performance depends on the evaluation data and recording conditions.
- Unseen voice-cloning methods may behave differently.
- Audio quality can affect reliability.
- Model scores are not automatically calibrated real-world probabilities.
- Borderline cases may require secondary verification.
- Real-time streaming deployment needs additional engineering.

---

## 📊 Evaluation Plan

Use a clearly separated test set and report:

| Metric | Purpose |
|---|---|
| Accuracy | Overall classification performance |
| Precision | Reliability of spoof predictions |
| Recall | Ability to detect spoofed samples |
| F1 | Balance between precision and recall |
| ROC-AUC | Ranking discrimination |
| EER | Standard anti-spoofing metric |
| FAR / FRR | Security and usability trade-off |
| Confusion Matrix | BONAFIDE vs SPOOF behaviour |
| Latency | Practical deployment performance |

**Important:** never claim an accuracy figure without specifying the dataset, test split, preprocessing, and evaluation procedure.

---

## 🧭 Roadmap

### Current
- [x] AASIST integration
- [x] Audio preprocessing
- [x] Multi-window inference
- [x] Risk aggregation
- [x] Explainability indicators
- [x] FastAPI backend
- [x] Interactive dashboard
- [x] CLI detector
- [x] Performance reporting

### Next
- [ ] Proper benchmark suite
- [ ] Larger multilingual evaluation
- [ ] Model calibration
- [ ] Replay-attack analysis
- [ ] Model ensemble
- [ ] Real-time microphone streaming
- [ ] Telephony / VoIP integration
- [ ] Edge inference optimization

---

## 📚 Research Basis

VoiceShield builds on research and open-source work in speech anti-spoofing, particularly AASIST and the wider ASVspoof ecosystem.

- AASIST: https://arxiv.org/abs/2110.01200
- ASVspoof: https://www.asvspoof.org/

Refer to the repository's `LICENSE`, `NOTICE`, and upstream project terms for attribution and licensing details.

---

## 👥 Team

### TeamRocket
**Smart India Hackathon 2026**  
**Problem Statement:** SIH26104

> Replace this section with your actual team-member names and institution before final submission.

---

## 📣 Project Pitch

> **VoiceShield turns voice-spoof detection from a black-box prediction into an interpretable, window-level risk assessment that helps humans understand, verify, and respond to suspicious audio.**

---

<div align="center">

### 🛡️ Detect. Explain. Protect.

**VoiceShield — making voice communication more trustworthy in the age of generative AI.**

</div>

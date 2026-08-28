VOICESHIELD — AI-POWERED REAL-TIME VOICE AUTHENTICITY DETECTION
Smart India Hackathon 2026 | Problem Statement SIH26104 | TeamRocket

============================================================
1. PROJECT OVERVIEW
============================================================

VoiceShield is an AI-powered voice authenticity analysis system designed
to detect synthetic, cloned, replayed, or spoofed speech.

The system uses the AASIST audio anti-spoofing model and performs
multi-window analysis instead of relying on only one prediction for an
entire recording.

VoiceShield produces:
- BONAFIDE / SPOOF verdict
- Overall policy risk score
- Bonafide and spoof scores
- Window-level timeline analysis
- Audio-quality information
- Explainability indicators
- Confidence/review band
- Recommended action
- Inference and processing performance

The project addresses SIH26104:
“AI-Powered Real-Time Detection and Prevention of Voice Cloning
Impersonation Attacks.”

============================================================
2. THE PROBLEM
============================================================

Modern voice-cloning and speech-synthesis systems can generate realistic
human speech. This creates security risks in:
- Phone calls
- Customer support
- Financial verification
- Authentication
- Social engineering
- Digital identity verification
- Fraudulent voice messages

A practical detector should do more than return one opaque percentage.
It should identify suspicious regions, consider recording quality, and
provide information that helps a human verify the result.

============================================================
3. OUR SOLUTION
============================================================

Audio Upload
    ↓
Validation
    ↓
Preprocessing / Resampling
    ↓
Overlapping Multi-Window Segmentation
    ↓
AASIST Inference
    ↓
Window-Level Spoof / Bonafide Scores
    ↓
Audio Quality + Temporal Analysis
    ↓
Risk Aggregation
    ↓
Explainability
    ↓
Final Dashboard Result

The current detector uses approximately 4-second windows with a 2-second
hop between windows.

============================================================
4. KEY FEATURES
============================================================

A. AI-BASED SPOOF DETECTION
Uses AASIST anti-spoofing inference to identify evidence associated with
synthetic or spoofed speech.

B. MULTI-WINDOW ANALYSIS
Long recordings are divided into overlapping windows so suspicious
evidence can be located in time.

C. WINDOW-LEVEL TIMELINE
Displays start/end time, bonafide score, spoof score, and label for each
window.

D. RISK ENGINE
Combines:
- Mean spoof score
- Median spoof score
- Peak spoof score
- High-risk window ratio
- Very-high-risk window ratio
- Audio quality
- Score dispersion / temporal variation

The result is a POLICY RISK SCORE, not a calibrated probability.

E. AUDIO QUALITY ASSESSMENT
Checks recording characteristics and exposes quality information rather
than silently treating every recording as equally reliable.

F. EXPLAINABILITY
Provides human-readable indicators such as:
- Strong spoof-model evidence
- Persistent suspicious evidence
- High temporal variation

G. CONFIDENCE / REVIEW BAND
Borderline cases can be marked for review instead of being presented as
certain decisions.

H. PERFORMANCE INFORMATION
Reports inference time, total processing time, analyzed windows, throughput,
and computing device.

============================================================
5. TECHNOLOGY STACK
============================================================

Backend:
- Python
- FastAPI
- Uvicorn
- NumPy
- PyTorch
- SoundFile
- SciPy
- AASIST

Frontend:
- HTML
- CSS
- JavaScript

Development:
- Visual Studio Code
- Git
- GitHub

============================================================
6. SYSTEM ARCHITECTURE
============================================================

User / Judge
     ↓
VoiceShield Web UI
     ↓
FastAPI API
     ↓
Detector
     ├── Preprocessing
     ├── Audio Quality Assessment
     ├── AASIST Model
     ├── Temporal / Window Analysis
     ├── Risk Engine
     └── Explainability
     ↓
JSON Response
     ↓
Dashboard

Important backend files:
- backend/detector.py — coordinates the complete detection pipeline
- backend/preprocessing.py — audio loading, resampling, windows
- backend/model.py — AASIST model interface
- backend/audio_quality.py — audio quality assessment
- backend/risk_engine.py — policy risk aggregation
- backend/explainability.py — human-readable indicators
- api_server.py — FastAPI service and endpoints

============================================================
7. PROJECT STRUCTURE
============================================================

SIH26104-TeamRocket-VoiceShield-9.5/
├── backend/
│   ├── __init__.py
│   ├── detector.py
│   ├── preprocessing.py
│   ├── model.py
│   ├── audio_quality.py
│   ├── explainability.py
│   ├── risk_engine.py
│   └── config.py
├── frontend/
│   ├── index.html
│   ├── app.js
│   └── styles.css
├── models/
├── config/
├── scripts/
│   └── run_detector.py
├── tests/
├── evaluation/
├── analysis/
├── api_server.py
├── predict.py
├── data_utils.py
├── evaluation.py
├── download_dataset.py
├── main.py
└── LICENSE

============================================================
8. API
============================================================

GET /
Serves the VoiceShield frontend.

GET /health
Returns service, model, device, and version information.

POST /predict
Accepts an audio file and returns the complete authenticity analysis.

Supported audio types:
- WAV
- FLAC
- OGG
- MP3

Maximum upload size:
50 MB

============================================================
9. HOW TO RUN LOCALLY
============================================================

1. Clone the repository:

git clone <YOUR_GITHUB_REPOSITORY_URL>
cd SIH26104-TeamRocket-VoiceShield-9.5

2. Create a virtual environment:

python -m venv .venv

3. Activate on Windows:

.venv\Scripts\activate

4. Install dependencies:

pip install -r requirements.txt

5. Start the server:

python -m uvicorn api_server:app --reload

6. Open:

http://127.0.0.1:8000

============================================================
10. COMMAND-LINE TEST
============================================================

Run:

python -m scripts.run_detector myvoice.wav

The command returns model, device, verdict, risk, audio, quality,
window-level, explainability, decision, and performance information.

============================================================
11. WHY MULTI-WINDOW ANALYSIS?
============================================================

Spoofing artefacts may not be equally visible throughout a recording.

Instead of hiding the complete recording inside one global score,
VoiceShield examines overlapping windows. This makes it possible to see:
- where suspicious evidence occurs
- whether suspicious evidence persists
- how model scores change over time

This provides more useful evidence for human verification.

============================================================
12. WHAT MAKES VOICESHIELD DIFFERENT?
============================================================

VoiceShield is designed as:

MODEL
  ↓
WINDOW-LEVEL EVIDENCE
  ↓
TEMPORAL ANALYSIS
  ↓
RISK ENGINE
  ↓
EXPLAINABILITY
  ↓
HUMAN REVIEW

The system separates raw model evidence from application-level risk policy.

This is important because a raw model score should not automatically be
presented as a guaranteed real-world probability.

============================================================
13. DEMO FLOW FOR JUDGES
============================================================

1. Open the VoiceShield dashboard.
2. Upload a genuine/bonafide recording.
3. Show the resulting risk assessment.
4. Upload a spoof/synthetic recording.
5. Compare verdict and risk.
6. Open the window-level timeline.
7. Point out suspicious time regions.
8. Show explainability indicators.
9. Show recommended action and confidence band.
10. Demonstrate CLI inference if needed:

python -m scripts.run_detector myvoice.wav

============================================================
14. JUDGE TALKING POINTS
============================================================

Q: What is your main innovation?

A: “VoiceShield does not rely on a single prediction for an entire
recording. It performs multi-window anti-spoofing analysis and aggregates
persistent evidence into an interpretable policy risk score while exposing
the timeline and reasons behind the result.”

Q: Why multi-window analysis?

A: “Voice-cloning artefacts may not be equally visible throughout an
entire recording. Window-level analysis helps identify temporal variation
and persistent suspicious regions.”

Q: Is the risk score a probability?

A: “No. It is a policy risk score built from AASIST window-level evidence.
It is not presented as a calibrated probability.”

Q: What happens with poor-quality audio?

A: “The system assesses audio quality separately and uses that information
conservatively in the risk pipeline. Quality information is also exposed
to the user.”

Q: How do you explain the result?

A: “We provide window-level scores, temporal analysis, risk indicators,
confidence bands, and recommended actions so users can understand and
verify the result.”

Q: Can it work in real time?

A: “The architecture uses short overlapping windows and batch inference,
making it suitable for near-real-time analysis. Processing performance is
also measured so the pipeline can be optimized for streaming deployment.”

============================================================
15. PRIVACY AND SECURITY
============================================================

The API temporarily processes uploaded files for inference and removes
the temporary file after processing.

For production deployment, add:
- Authentication
- HTTPS
- Rate limiting
- Access control
- Encryption
- Secure logging
- Retention policies
- Consent/privacy controls

============================================================
16. LIMITATIONS
============================================================

VoiceShield should not be presented as a perfect detector.

Limitations include:
- Performance depends on training/evaluation data.
- New unseen cloning methods may reduce performance.
- Recording quality can affect reliability.
- Model scores are not automatically calibrated probabilities.
- Borderline cases may require secondary verification.
- Streaming deployment requires additional engineering.
- Production use requires stronger security and privacy controls.

============================================================
17. FUTURE SCOPE
============================================================

1. Real-time microphone/streaming detection
2. Model ensembles
3. Continuous evaluation against new spoofing techniques
4. Advanced spectrogram/time-frequency explainability
5. Edge/on-device deployment
6. VoIP/telephony integration
7. Evaluation across Indian languages and accents
8. Adversarial robustness testing
9. Security operations integration
10. Proper probability calibration

============================================================
18. EVALUATION
============================================================

Recommended metrics:
- Accuracy
- Precision
- Recall
- F1-score
- ROC-AUC
- Equal Error Rate (EER)
- False Acceptance Rate (FAR)
- False Rejection Rate (FRR)
- Confusion matrix
- Inference latency
- Throughput

When adding benchmark numbers, always specify the dataset, test split,
preprocessing, and evaluation method.

Dataset:
[INSERT DATASET]

Test samples:
[INSERT NUMBER]

Accuracy:
[INSERT MEASURED VALUE]

Precision:
[INSERT MEASURED VALUE]

Recall:
[INSERT MEASURED VALUE]

F1-score:
[INSERT MEASURED VALUE]

EER:
[INSERT MEASURED VALUE]

Inference latency:
[INSERT MEASURED VALUE]

IMPORTANT:
Do not claim “100% accuracy” or “guaranteed detection” without rigorous
evaluation evidence.

============================================================
19. REPRODUCIBILITY
============================================================

Document:
- Dataset and version
- Train/validation/test split
- Speaker-disjoint split where appropriate
- Sampling rate
- Window size
- Hop size
- Model checkpoint
- Random seeds
- Hardware
- Python/package versions
- Evaluation script
- Metrics

============================================================
20. CURRENT PROJECT STATUS
============================================================

[✓] AASIST-based spoof detection
[✓] Multi-window audio analysis
[✓] Audio preprocessing
[✓] Audio-quality assessment
[✓] Risk aggregation
[✓] Explainability indicators
[✓] FastAPI backend
[✓] Web dashboard
[✓] Window-level visualization
[✓] Command-line detector
[✓] Performance reporting

Future:
[ ] Real-time microphone streaming
[ ] Production authentication
[ ] Larger multilingual evaluation
[ ] Model ensemble
[ ] Advanced calibration
[ ] Telephony integration

============================================================
21. TEAM
============================================================

Team: TeamRocket
Problem Statement: SIH26104
Event: Smart India Hackathon 2026

Team members:
- [MEMBER 1]
- [MEMBER 2]
- [MEMBER 3]
- [MEMBER 4]

Institution:
[INSTITUTION NAME]

============================================================
22. SHORT GITHUB DESCRIPTION
============================================================

AI-powered voice authenticity detection using AASIST, multi-window
analysis, explainable risk scoring, and a FastAPI web dashboard.

============================================================
23. ONE-LINE PITCH
============================================================

“VoiceShield turns voice-spoofing detection from a black-box prediction
into an interpretable, window-level risk assessment that helps humans
understand, verify, and respond to suspicious audio.”

============================================================
24. FINAL README CHECKLIST
============================================================

Before publishing README.md:

[ ] Add repository URL
[ ] Add team members
[ ] Add institution
[ ] Add actual dataset
[ ] Add measured evaluation results
[ ] Add dashboard screenshot
[ ] Add demo video/GIF
[ ] Add deployed demo link if available
[ ] Add installation/dependency instructions
[ ] Add model attribution/citation
[ ] Verify license
[ ] Verify all commands
[ ] Do not make unsupported accuracy claims

============================================================
END OF VOICESHIELD README CONTENT
============================================================

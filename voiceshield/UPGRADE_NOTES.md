# VoiceShield 9.5-oriented upgrade

This package keeps the original AASIST project and its original `predict.py` path intact while adding a separate product layer.

## Added

- `backend/`: reusable multi-window inference and risk pipeline
- `api_server.py`: local FastAPI service + frontend host
- `frontend/`: zero-build interactive browser UI
- microphone recording encoded to WAV in-browser
- drag/drop upload and audio preview
- segment-level suspicion timeline
- segment inspector
- quality diagnostics
- structured evidence indicators
- borderline/review band
- latency and device telemetry
- benchmark scaffolding
- automated unit tests
- Windows launch scripts

## Deliberate design choice

The UI does not claim that a softmax score is a calibrated probability. The product displays model evidence, a policy risk score, and a review recommendation separately.

## Frontend safety

No existing frontend files were edited. The new interface is isolated under `frontend/` and is served by `api_server.py` at `/`.

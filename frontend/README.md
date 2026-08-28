# VoiceShield Frontend

A zero-build, dependency-free browser UI for the VoiceShield backend.

## Start

From the repository root:

```powershell
python -m uvicorn api_server:app --host 127.0.0.1 --port 8000
```

Open `http://127.0.0.1:8000`.

## Interactive features

- drag-and-drop audio upload
- audio preview
- browser microphone recording (encoded to WAV in-browser)
- one-click multi-window analysis
- animated risk gauge
- clickable segment timeline
- segment inspector
- recording-quality panel
- model/device and latency reporting

No frontend framework or Node.js install is required.

# VoiceShield frontend
Replace the existing `frontend` folder with this folder.
From the project root run:
`.\.venv\Scripts\Activate.ps1`
`python -m uvicorn api_server:app --reload`
Open http://127.0.0.1:8000
The frontend calls the existing `/health` and `/predict` endpoints. It supports drag/drop, audio preview, waveform, model results, risk score, window analysis, explainability, JSON output and local history. If the API is offline, a clearly labelled demo fallback is shown.

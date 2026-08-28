from __future__ import annotations

import os
import tempfile
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from backend.detector import Detector

ROOT = Path(__file__).resolve().parent
FRONTEND = ROOT / "frontend"
MAX_UPLOAD_BYTES = 50 * 1024 * 1024
ALLOWED_EXTENSIONS = {".wav", ".flac", ".ogg", ".mp3"}

app = FastAPI(title="VoiceShield API", version="2.0.0", description="Multi-window AASIST voice authenticity analysis")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

detector = Detector()

if FRONTEND.exists():
    app.mount("/assets", StaticFiles(directory=str(FRONTEND)), name="assets")


@app.get("/", include_in_schema=False)
def home():
    return FileResponse(FRONTEND / "index.html")


@app.get("/health")
def health():
    return {
        "status": "ok",
        "model": "AASIST",
        "device": detector.model.device_name,
        "version": app.version,
    }


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    suffix = Path(file.filename or "audio.wav").suffix.lower()
    if suffix not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"Unsupported audio type: {suffix}. Use WAV, FLAC, OGG or MP3.")

    temp_path = None
    total = 0
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            temp_path = tmp.name
            while chunk := await file.read(1024 * 1024):
                total += len(chunk)
                if total > MAX_UPLOAD_BYTES:
                    raise HTTPException(status_code=413, detail="Audio file is larger than the 50 MB limit.")
                tmp.write(chunk)
        result = detector.analyze(temp_path)
        result["input"] = {"filename": file.filename, "size_bytes": total}
        return result
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    finally:
        if temp_path:
            try:
                os.remove(temp_path)
            except OSError:
                pass

@app.get("/styles.css", include_in_schema=False)
def styles():
    return FileResponse(FRONTEND / "styles.css", media_type="text/css")


@app.get("/app.js", include_in_schema=False)
def javascript():
    return FileResponse(FRONTEND / "app.js", media_type="application/javascript")

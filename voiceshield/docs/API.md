# API

Start:

```powershell
uvicorn api_server:app --host 127.0.0.1 --port 8000
```

## GET `/health`

Returns service/model/device status.

## POST `/predict`

Multipart form upload:

- field: `file`
- accepted: wav, flac, ogg, mp3

The response includes the verdict, risk score, audio metadata, quality assessment, per-window scores, indicators, and performance metrics.

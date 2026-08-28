# VoiceShield backend architecture

The original AASIST model and frontend remain separate. This layer adds robust application inference around the pretrained detector.

```text
Audio file / stream
      |
      v
Decode + mono + resample 16 kHz
      |
      v
Quality analysis
      |
      v
Sliding 4.0375 s windows
      |
      v
AASIST inference on GPU/CPU
      |
      +---- per-window bonafide/spoof scores
      |
      v
Risk aggregation
      |
      +---- mean evidence
      +---- high-risk persistence
      +---- peak evidence
      +---- quality-aware adjustment
      |
      v
Verdict + indicators + latency
```

The risk score is a **policy-layer score**, not a calibrated probability of deception. For deployment, it must be calibrated and validated on representative data.

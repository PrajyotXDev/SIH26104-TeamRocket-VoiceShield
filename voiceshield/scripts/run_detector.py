from __future__ import annotations

import argparse
import json

from backend.detector import Detector


def main():
    parser = argparse.ArgumentParser(description="Run multi-window AASIST analysis")
    parser.add_argument("audio", help="Path to an audio file")
    parser.add_argument("--hop", type=float, default=2.0, help="Window hop in seconds")
    args = parser.parse_args()

    result = Detector().analyze(args.audio, hop_seconds=args.hop)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

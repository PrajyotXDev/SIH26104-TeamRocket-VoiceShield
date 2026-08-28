from __future__ import annotations

import json
from pathlib import Path

import torch

from models.AASIST import Model

from .config import CONFIG_PATH, MODEL_PATH


class AASISTModel:
    def __init__(self, config_path: Path = CONFIG_PATH, model_path: Path = MODEL_PATH):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        with open(config_path, "r", encoding="utf-8") as fh:
            config = json.load(fh)
        self.model = Model(config["model_config"])
        state = torch.load(model_path, map_location=self.device, weights_only=True)
        self.model.load_state_dict(state)
        self.model.to(self.device)
        self.model.eval()

    @property
    def device_name(self) -> str:
        if self.device.type == "cuda":
            return torch.cuda.get_device_name(0)
        return "CPU"

    def predict_batch(self, batch_audio):
        x = torch.as_tensor(batch_audio, dtype=torch.float32, device=self.device)
        with torch.inference_mode():
            _, logits = self.model(x)
            probs = torch.softmax(logits, dim=1)
        return probs.detach().cpu().numpy()

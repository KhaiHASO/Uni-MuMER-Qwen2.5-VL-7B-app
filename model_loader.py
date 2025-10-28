"""
Minimal TAMER loader stub.
Replace `load_tamer_model` implementation with actual TAMER code when integrating.
"""

import os
from typing import Optional
from PIL import Image

from config import MODEL_DIR, CHECKPOINT_FILENAME, IMAGE_MAX_SIZE, DEVICE


class TamerModel:
    def __init__(self, model_dir: str = MODEL_DIR, checkpoint_filename: str = CHECKPOINT_FILENAME):
        self.model_dir = model_dir
        self.checkpoint_path = os.path.join(model_dir, checkpoint_filename)
        self.model = None

    def load(self) -> bool:
        if not os.path.isdir(self.model_dir):
            return False
        if not os.path.isfile(self.checkpoint_path):
            return False
        # TODO: integrate actual TAMER architecture and load weights here
        # self.model = ...
        self.model = "loaded"
        return True

    def infer(self, image: Image.Image) -> Optional[str]:
        if self.model is None:
            return None
        # TODO: real preprocessing, encoder-decoder, and LaTeX decoding
        return "\\frac{a}{b} + c"  # placeholder


def load_tamer_model() -> Optional[TamerModel]:
    model = TamerModel()
    if model.load():
        return model
    return None



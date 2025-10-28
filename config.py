"""
Config for TAMER: Tree-Aware Transformer for HME Recognition
"""

import os


class Config:
    # App
    APP_TITLE = "TAMER Demo - Handwritten Math Expression Recognition"

    # Paths
    PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
    # Directory containing trained TAMER checkpoint(s)
    MODEL_DIR = os.getenv("TAMER_MODEL_DIR", os.path.join(PROJECT_DIR, "weights"))
    # Default checkpoint filename (update to your actual file)
    CHECKPOINT_FILENAME = os.getenv("TAMER_CHECKPOINT", "tamer_hmer.ckpt")

    # Inference
    IMAGE_MAX_SIZE = (1024, 1024)
    DEVICE = os.getenv("DEVICE", "cuda" if os.getenv("CUDA_VISIBLE_DEVICES") else "cpu")


# Convenience exports
APP_TITLE = Config.APP_TITLE
MODEL_DIR = Config.MODEL_DIR
CHECKPOINT_FILENAME = Config.CHECKPOINT_FILENAME
IMAGE_MAX_SIZE = Config.IMAGE_MAX_SIZE
DEVICE = Config.DEVICE

 

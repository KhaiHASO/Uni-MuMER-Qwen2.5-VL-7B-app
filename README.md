# TAMER Demo: Handwritten Mathematical Expression Recognition

A minimal Streamlit demo scaffolding for TAMER (Tree-Aware Transformer for HME Recognition). This repo provides a lightweight UI and placeholders to integrate the official TAMER implementation and checkpoints.

## What’s included
- Streamlit UI (`app.py`) for uploading an image and displaying LaTeX output
- Config (`config.py`) for paths and settings
- Loader stub (`model_loader.py`) you will replace with real TAMER code
- Minimal `requirements.txt`

## Quickstart

1) Create and activate environment (example with conda):
```bash
conda create -n tamer-demo python=3.10 -y
conda activate tamer-demo
pip install -r requirements.txt
```

2) Place your TAMER checkpoint:
- Put your checkpoint in `weights/` (create the folder if missing), e.g. `weights/tamer_hmer.ckpt`
- Or set environment variables:
  - `TAMER_MODEL_DIR` to the directory containing the checkpoint
  - `TAMER_CHECKPOINT` to the filename of the checkpoint

3) Run the app:
```bash
streamlit run app.py
```
Open the displayed localhost URL in your browser.

## Integrating the real TAMER model
Replace the placeholder implementation in `model_loader.py`:
- Implement the TAMER architecture
- Load the checkpoint (Lightning/PyTorch)
- Add preprocessing (resize, binarization, normalization if required)
- Implement decoding to LaTeX (tokenizer/grammar as per TAMER)

Example shape of code to implement:
```python
class TamerModel:
    def load(self):
        self.model = ...  # init TAMER
        state = torch.load(self.checkpoint_path, map_location='cpu')
        self.model.load_state_dict(state['state_dict'] or state)
        self.model.eval()
        return True

    def infer(self, image: Image.Image) -> str:
        tensor = preprocess(image)
        with torch.no_grad():
            logits = self.model(tensor)
        return decode_latex(logits)
```

## Notes
- This demo intentionally avoids bundling heavy model code; link or vendor in the upstream TAMER implementation you prefer.
- GPU support depends on your local PyTorch install. Update `requirements.txt` if you need specific CUDA wheels.

## License
This demo scaffold is provided under the MIT License.

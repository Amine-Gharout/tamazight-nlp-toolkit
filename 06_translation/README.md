# 06 — Machine Translation

Kabyle translation using Meta's NLLB-200 (No Language Left Behind) with CTranslate2 for efficient inference.

## Contents

```
models/      → NLLB-200-3.3B converted to CTranslate2 format
notebooks/   → Translation inference notebooks
outputs/     → Generated translations
```

| File | Description |
|------|-------------|
| `notebooks/translate_src_to_pivot.ipynb` | Translates English→Kabyle and French→Kabyle via NLLB |
| `notebooks/inference/nllb_ctranslate2_inference.ipynb` | Low-VRAM inference with CTranslate2 quantization |

## Method

Uses English/French as pivot languages → NLLB-200-3.3B → Kabyle. CTranslate2 provides int8/float16 quantization for running on limited GPU memory (3.5–6.5 GB).

## Download & Install the NLLB Model

The NLLB-200-3.3B model is **not stored in git** (too large). Download it from HuggingFace
using the provided script. The script pulls a **pre-converted CTranslate2** version, so no
manual conversion is needed — just download and use.

### Prerequisites

```bash
# Install huggingface_hub (only package needed for download)
pip install huggingface_hub

# Optional: install CTranslate2 for inference later
pip install ctranslate2
```

### Step-by-Step

```bash
cd /path/to/chat_aqvayli

# Option A — float16 (~6.5 GB, best translation quality, needs ~7 GB GPU RAM)
python scripts/download_nllb_model.py

# Option B — int8 (~3.5 GB, good quality, needs ~4 GB GPU RAM, recommended for consumer GPUs)
python scripts/download_nllb_model.py --quant int8_float16
```

The model lands at `06_translation/models/nllb-200-3.3B-ct2/`.

### Verify the Download

```bash
ls -lh 06_translation/models/nllb-200-3.3B-ct2/
# Expected files:
#   config.json       (~1 KB)       model configuration
#   model.bin         (~6.5 or 3.5 GB)  model weights
#   sentencepiece.bpe.model   (~5 MB)   tokenizer
#   tokenizer.json    (~4 MB)       tokenizer config
#   shared_vocabulary.txt        vocabulary file
```

### Use in Python / Notebooks

```python
import ctranslate2

# Point to your downloaded model
CT2_MODEL_PATH = "06_translation/models/nllb-200-3.3B-ct2"

translator = ctranslate2.Translator(str(CT2_MODEL_PATH), device="cuda")

# Translate: English → Kabyle (kab_Latn)
output = translator.translate_batch(
    [["Hello, how are you?"]],
    target_prefix=[["kab_Latn"]],
)
print(output[0].hypotheses[0])
```

### Troubleshooting

| Problem | Solution |
|---------|----------|
| `ImportError: huggingface_hub` | `pip install huggingface_hub` |
| `403 Forbidden` / `401 Unauthorized` | Run `huggingface-cli login` then retry |
| `CUDA out of memory` | Use `--quant int8_float16` or set `device="cpu"` |
| Download hangs | Press Ctrl+C and re-run — `resume_download=True` is enabled |
| Model already exists message | Use `--force` to re-download from scratch |

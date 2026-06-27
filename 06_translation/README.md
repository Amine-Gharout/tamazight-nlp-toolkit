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

## Download Model

```bash
python scripts/download_nllb_model.py              # float16 (~6.5 GB)
python scripts/download_nllb_model.py --quant int8  # int8 (~3.5 GB)
```

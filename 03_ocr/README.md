# 03 — Optical Character Recognition (OCR)

Digitizing physical Kabyle texts from scanned documents/images using multimodal LLMs.

## Contents

```
prompts/         → Shared system prompts with linguistic rules
scripts/         → Python scripts for batch OCR
notebooks/       → Jupyter notebooks for interactive OCR experiments
outputs/         → Extracted text outputs organized by model
```

| File | Description |
|------|-------------|
| `prompts/lrl_ocr_prompt.py` | Expert prompt with Kabyle grammar rules (y vs ɣ, diacritics) |
| `scripts/ocr_kabyle_gemini.py` | Batch OCR using Gemini 2.5 Pro (uses `shared/gemini_utils.py`) |
| `notebooks/google_ocr.ipynb` | OCR with Google Gemini (Flash & Pro) |
| `notebooks/google_ocr_corrected.ipynb` | OCR with grammar-based post-correction |
| `notebooks/qwen_ocr.ipynb` | OCR with Qwen-VL (7B & 72B) |

## Key Challenge — `y` vs `ɣ`

Kabyle uses both `y` (palatal /j/) and `ɣ` (uvular /ɣ/) which look similar in print. The prompt uses grammatical rules (verb conjugation, word roots) to disambiguate, not just visual recognition.

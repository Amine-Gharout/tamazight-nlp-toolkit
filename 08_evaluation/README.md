# 08 — Evaluation

Benchmarking translation quality using FLORES+ devtest and chrF++ metrics.

## Contents

| File | Description |
|------|-------------|
| `benchmarks/nllb_benchmark_flores.ipynb` | Evaluates NLLB translation on FLORES+ French→Tamazight/Kabyle test set |
| `benchmarks/get_least.ipynb` | Analyzes worst-performing translations for error patterns |

## Metric

**chrF++** — Character n-gram F-score with word order. Preferred over BLEU for morphologically rich languages like Tamazight/Kabyle, as it captures partial morphological matches.

## Data

FLORES+ devtest: ~1,000 parallel French–Tamazight/Kabyle sentences used as reference translations.

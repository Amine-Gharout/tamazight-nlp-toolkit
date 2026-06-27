# 05 — Data Cleaning

Cleaning and curating parallel corpora for Tamazight/Kabyle NLP tasks.

## Contents

| File | Description |
|------|-------------|
| `cleaners/clean_tab_pairs.py` | Removes malformed tab-separated pairs |
| `cleaners/remove_single_sentences.py` | Filters out unpaired/isolated sentences |
| `cleaners/replace_tabs.py` | Normalizes tab/whitespace formatting |
| `cleaners/rm_fr_en_rows.ipynb` | Removes French/English rows from Tamazight/Kabyle data |
| `cleaners/size_sentence.ipynb` | Filters sentences by length constraints |

## Purpose

Raw crawled/extracted data contains formatting issues, mixed languages, and incomplete pairs. These scripts prepare clean parallel corpora for translation model training and evaluation.

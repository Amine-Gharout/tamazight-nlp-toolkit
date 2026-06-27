# 04 — Automatic Speech Recognition (ASR)

Transcribing Kabyle speech from audio files and live radio streams.

## Contents

```
scripts/     → Python scripts for batch audio transcription
notebooks/   → Interactive notebooks for live/recorded transcription
```

| File | Description |
|------|-------------|
| `scripts/transcribe_kabyle_gemini.py` | Batch transcription of Kabyle audio via Gemini 2.5 Pro (uses `shared/gemini_utils.py`) |
| `notebooks/live_radio_transcription.ipynb` | Real-time transcription of Radio Chaine 2 with API key rotation |

## Method

Uses Google Gemini 2.5 Pro with a specialized prompt that encodes Kabyle linguistic rules (diacritics, y vs ɣ distinction) for accurate transcription.

The live pipeline uses 15 Gemini API keys with automatic rotation to handle rate limits during continuous streaming.

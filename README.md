# Low Resource Language Toolkit 🌍

This repository contains reusable tools, notebooks, and pipelines designed for NLP research involving Low-Resource Languages (LRLs). Originally formulated for Tamazight/Kabyle, the structural pipelines herein (OCR, translation, Retrieval-Augmented Translation) can be seamlessly adapted to any low-resource language pairs with minimal modifications. 

## Project Structure

- `0_data/`: Raw datasets, cleaned files, and indexed corpora (parallel text `.txt` pairs)
- `01_data_collection/`: Scraping podcasts + downloading parallel data from MADLAD-400 / Tatoeba
- `02_language_id/`: Language identification filtering (GlotLID, Meta MMS)
- `03_ocr/`: Optical Character Recognition via Gemini & Qwen VL (prompts, scripts, notebooks, outputs)
- `04_asr/`: Automatic Speech Recognition — batch transcription + live radio pipeline
- `05_data_cleaning/`: Cleaning and curating parallel corpora (tab cleanup, dedup, filtering)
- `06_translation/`: Machine translation using NLLB-200-3.3B with CTranslate2 fast inference
- `07_rat/`: Retrieval-Augmented Translation (FAISS + LangChain + Gemini)
- `08_evaluation/`: Translation quality benchmarks (FLORES+, chrF++)
- `09_deployment/`: Azure cloud infrastructure for 24/7 radio recording

## Setup Requirements

Ensure you meet the required dependencies:

```bash
pip install -r requirements.txt
```

### Download Data & Models

Large files (datasets and NLLB model) are **not stored in git**. Download them:

```bash
# 1. Download raw datasets (~619 MB) from Google Drive
bash scripts/download_data.sh

# 2. Download NLLB-200-3.3B CTranslate2 model (~6.5 GB) from HuggingFace
python scripts/download_nllb_model.py                       # float16 (best quality)
python scripts/download_nllb_model.py --quant int8_float16  # int8 (less VRAM)
```

> **First-time setup:** If you're the repo owner, run `bash scripts/pack_data.sh` to create `raw_data.tar.gz`, upload it to Google Drive, then paste the file ID into `scripts/download_data.sh`.

## Technologies & Frameworks Used

This toolkit leverages several state-of-the-art technologies to achieve high-quality results for under-represented languages:

- [**NLLB-200 (No Language Left Behind)**](https://ai.meta.com/research/no-language-left-behind/): Meta's revolutionary machine translation model capable of translating across 200+ languages—crucial for serving as a foundation or pivot translation model for low-resource tasks.
- [**CTranslate2**](https://opennmt.net/CTranslate2/): A fast inference engine utilizing weight quantization (such as INT8 and FP16), radically reducing memory usage while accelerating prediction speeds for Transformer models like NLLB.
- [**FAISS (Facebook AI Similarity Search)**](https://faiss.ai/): A wildly efficient library for dense vector similarity search and clustering. In this repository, it acts as the memory bank to fetch the most similar human-translated source/target sentence pairs.
- [**LangChain**](https://www.langchain.com/): Used to orchestrate the Retrieval-Augmented Generation (RAG / RAT) pipeline, fluidly connecting FAISS indices, Prompts, and backend LLMs.
- **Multimodal LLMs ([Google Gemini Series](https://deepmind.google/technologies/gemini/) & [Qwen-VL](https://github.com/QwenLM/Qwen-VL))**: Powerful vision-language models utilized to tackle complex physical OCR challenges—specifically deciphering scans of old books natively written in less-represented alphabets or languages.

## Environment

Copy `.env.example` to `.env` and configure your necessary API keys before running the notebooks (OCR, RAT pipelines).

## Adapting to Your Target Language
Throughout the codebase, variables frequently list paths to `kab` (Tamazight/Kabyle) or `fra` (French) pairs. You can replace the ISO codes arrays across scripts (like `LANG_CODES`) and change dataset paths matching your specified source/target parallel corpora.

## Usage

1. **Data Collection** (`01_data_collection/`): Gather parallel data via scraping or download.
2. **Language ID** (`02_language_id/`): Filter collected data for target language.
3. **OCR** (`03_ocr/`): Digitize physical documents using Gemini or Qwen VL.
4. **ASR** (`04_asr/`): Transcribe audio — batch files or live radio stream.
5. **Data Cleaning** (`05_data_cleaning/`): Clean and curate parallel corpora.
6. **Translation** (`06_translation/`): Run NLLB-200 inference with CTranslate2.
7. **RAT** (`07_rat/`): Enhance translations via FAISS + LangChain + Gemini.
8. **Evaluation** (`08_evaluation/`): Benchmark quality with FLORES+ / chrF++.
9. **Deployment** (`09_deployment/`): Deploy 24/7 radio recorder on Azure.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## Acknowledgements

This work was completed during a research internship at the **CEDRIC Laboratory** at **Le Cnam (Conservatoire National des Arts et Métiers) de Paris**, focusing on the preservation and digitization of Low-Resource Languages, starting with the Tamazight/Kabyle language. Special thanks to the open-source community for tools like NLLB, CTranslate2, and LangChain that made this pipeline possible.

## License

This project is open-source and available under the [MIT License](LICENSE).


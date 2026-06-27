# 07 — Retrieval-Augmented Translation (RAT)

Improving translation quality by retrieving similar human-translated sentence pairs as few-shot context for LLMs.

## Contents

| File | Description |
|------|-------------|
| `notebooks/rat_gemini_langchain.ipynb` | RAT pipeline: FAISS + BGE-M3 embeddings + Gemini |
| `notebooks/rat_pivot_to_target.ipynb` | Pivot-based RAT (source → pivot → target) |

## Architecture

```
Parallel Corpus (fr_kab.txt)
        │
        ▼
  BGE-M3 Embeddings
        │
        ▼
  FAISS Index ───► Retrieve top-k similar pairs
                        │
                        ▼
              Gemini LLM (few-shot prompt)
                        │
                        ▼
                 Translation
```

## Tech Stack

- **FAISS**: Dense vector search for similar pair retrieval
- **BGE-M3**: Multilingual embedding model
- **LangChain**: Orchestration of retrieval + generation
- **Gemini**: Final translation LLM with few-shot context

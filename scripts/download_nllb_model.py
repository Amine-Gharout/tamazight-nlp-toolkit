#!/usr/bin/env python3
"""
Download NLLB-200-3.3B CTranslate2 Model from HuggingFace

Usage:
    python scripts/download_nllb_model.py                        # float16 (~6.5 GB)
    python scripts/download_nllb_model.py --quant int8_float16   # int8 (~3.5 GB, less VRAM)

This downloads a pre-converted CTranslate2 model for fast low-VRAM inference.
After downloading, the model is placed at: 06_translation/models/nllb-200-3.3B-ct2/
"""

import os
import sys
import argparse
from pathlib import Path

# -- Config --
PROJECT_ROOT = Path(__file__).resolve().parent.parent
MODEL_DIR = PROJECT_ROOT / "06_translation" / "models" / "nllb-200-3.3B-ct2"

# Pre-converted CTranslate2 repos on HuggingFace (by JustFrederik, well-maintained)
CT2_REPOS = {
    "float16": "JustFrederik/nllb-200-3.3B-ct2-float16",       # ~6.5 GB, best quality
    "int8_float16": "JustFrederik/nllb-200-3.3B-ct2-int8",     # ~3.5 GB, good quality
}


def download_model(repo_id: str, target_dir: Path):
    """Download a pre-converted CTranslate2 model from HuggingFace."""
    from huggingface_hub import snapshot_download

    print(f"Repository: {repo_id}")
    print(f"Target:     {target_dir}")
    print()

    target_dir.mkdir(parents=True, exist_ok=True)

    snapshot_download(
        repo_id=repo_id,
        local_dir=str(target_dir),
        resume_download=True,
        local_files_only=False,
    )

    print(f"\nDone! Model saved to: {target_dir}")

    # Show what was downloaded
    total_size = 0
    for f in sorted(target_dir.iterdir()):
        if f.is_file():
            size_mb = f.stat().st_size / (1024 * 1024)
            total_size += size_mb
            print(f"  {f.name}: {size_mb:.1f} MB")
    print(f"  Total: {total_size:.1f} MB")


def verify_model(target_dir: Path):
    """Basic verification that model files exist."""
    required = ["model.bin", "config.json"]
    missing = [f for f in required if not (target_dir / f).exists()]
    if missing:
        print(f"WARNING: Missing expected files: {missing}")
        print("The model may still work if structure differs.")
    else:
        print("Model files look complete.")


def main():
    parser = argparse.ArgumentParser(
        description="Download NLLB-200-3.3B CTranslate2 model from HuggingFace"
    )
    parser.add_argument(
        "--quant", choices=list(CT2_REPOS.keys()), default="float16",
        help="Quantization level: float16 (~6.5 GB, best quality) or int8_float16 (~3.5 GB, good)"
    )
    parser.add_argument(
        "--force", action="store_true",
        help="Re-download even if model already exists"
    )
    args = parser.parse_args()

    if MODEL_DIR.exists() and any(MODEL_DIR.iterdir()) and not args.force:
        print(f"Model already exists at: {MODEL_DIR}")
        print("Use --force to re-download.")
        verify_model(MODEL_DIR)
        return

    repo_id = CT2_REPOS[args.quant]
    print(f"Downloading NLLB-200-3.3B CTranslate2 ({args.quant})...")
    print(
        f"This will download ~{'3.5' if 'int8' in args.quant else '6.5'} GB.\n")

    try:
        download_model(repo_id, MODEL_DIR)
        print("\nSUCCESS! Model is ready for inference.")
        print(f"Use in notebooks: CT2_MODEL_PATH = '{MODEL_DIR}'")
    except ImportError:
        print("ERROR: huggingface_hub is not installed.")
        print("Install it with: pip install huggingface_hub")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR during download: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

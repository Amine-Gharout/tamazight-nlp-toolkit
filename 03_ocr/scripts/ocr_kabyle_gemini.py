"""
Batch OCR of Kabyle documents using Gemini.

Usage:
    export GEMINI_API_KEY='your-key-here'
    python scripts/ocr_kabyle_gemini.py -i doc -o outputs/gemini
"""

from shared.gemini_utils import GeminiProcessor
import argparse
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))


# ─── Kabyle OCR System Prompt ───
SYSTEM_PROMPT = r"""
You are an expert OCR system specialized in Kabyle (Amazigh/Berber) language text extraction. Extract ALL text from this image with maximum accuracy, preserving the original layout and structure.

CRITICAL: Kabyle uses special diacritical characters that MUST be preserved exactly:
- Consonants with underdots: ḍ ṛ ṣ ṭ ẓ
- Consonants with other marks: ḥ ɛ ɣ č ǧ
- Digraphs: ch, kh, gh, gw, kw

IMPORTANT DISTINCTION - DO NOT CONFUSE:
- 'y' (Latin letter y) and 'ɣ' (gamma/ghain) are DIFFERENT letters
- 'y' is the regular Latin letter y (U+0079)
- 'ɣ' is the gamma character (U+0263), representing a voiced velar fricative
- Pay close attention to distinguish between these two characters in the text

Output requirements:
1. Preserve all diacritical marks precisely (dots under letters, special characters)
2. Maintain original line breaks and paragraph structure
3. If any character is unclear, mark it with [?] but continue extraction
4. Output the text in a structured format (e.g., line-by-line or paragraph-by-paragraph)
5. Do not translate, interpret, or modify the text—only extract what you see

Extract the text now:
"""


def main():
    parser = argparse.ArgumentParser(
        description="Batch OCR of Kabyle documents using Gemini")
    parser.add_argument("--input-dir", "-i", default="doc",
                        help="Directory containing images to OCR (default: doc)")
    parser.add_argument("--output-dir", "-o", default="outputs/gemini",
                        help="Directory to save OCR results (default: outputs/gemini)")
    parser.add_argument("--model", "-m", default="gemini-2.5-pro",
                        choices=["gemini-2.5-pro", "gemini-2.5-flash"],
                        help="Gemini model version (default: gemini-2.5-pro)")
    parser.add_argument("--extensions", "-e", nargs="+",
                        default=[".png", ".jpg", ".jpeg",
                                 ".webp", ".bmp", ".tiff"],
                        help="File extensions to process (default: .png .jpg .jpeg .webp .bmp .tiff)")
    args = parser.parse_args()

    processor = GeminiProcessor(model_name=args.model)

    print(f"📄 OCR Pipeline — Kabyle Document Digitization")
    print(f"   Input:  {args.input_dir}")
    print(f"   Output: {args.output_dir}")
    print(f"   Model:  {args.model}")
    print()

    processor.process_directory(
        input_dir=args.input_dir,
        output_dir=args.output_dir,
        system_prompt=SYSTEM_PROMPT,
        extensions=tuple(ext.lower() for ext in args.extensions),
    )


if __name__ == "__main__":
    main()

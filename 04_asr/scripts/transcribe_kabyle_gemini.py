"""
Batch transcription of Kabyle audio using Gemini.

Usage:
    export GEMINI_API_KEY='your-key-here'
    python scripts/transcribe_kabyle_gemini.py -i audio -o outputs
"""

from shared.gemini_utils import GeminiProcessor
import argparse
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))


# ─── Kabyle ASR System Prompt ───
SYSTEM_PROMPT = r"""
You are an expert transcription system specialized in Kabyle (Amazigh/Berber) language audio transcription. Transcribe ALL speech from this audio file with maximum accuracy, preserving the natural flow and structure.

CRITICAL: Kabyle uses special diacritical characters that MUST be preserved exactly:
- Consonants with underdots: ḍ ṛ ṣ ṭ ẓ
- Consonants with other marks: ḥ ɛ ɣ č ǧ
- Digraphs: ch, kh, gh, gw, kw

IMPORTANT DISTINCTION - DO NOT CONFUSE:
- 'y' (Latin letter y) and 'ɣ' (gamma/ghain) are DIFFERENT letters
- 'y' is the regular Latin letter y (U+0079)
- 'ɣ' is the gamma character (U+0263), representing a voiced velar fricative
- Pay close attention to distinguish between these two phonemes in the speech

Output requirements:
1. Preserve all diacritical marks precisely (dots under letters, special characters)
2. Maintain natural speech flow with appropriate paragraph breaks
3. If any word is unclear, mark it with [?] but continue transcription
4. Output the text in a structured format (paragraph-by-paragraph)
5. Do not translate, interpret, or modify the speech—only transcribe what you hear
6. Include speaker changes if multiple speakers are present

Transcribe the audio now:
"""


def main():
    parser = argparse.ArgumentParser(
        description="Batch transcription of Kabyle audio using Gemini")
    parser.add_argument("--input-dir", "-i", default="audio",
                        help="Directory containing audio files to transcribe (default: audio)")
    parser.add_argument("--output-dir", "-o", default="outputs",
                        help="Directory to save transcriptions (default: outputs)")
    parser.add_argument("--model", "-m", default="gemini-2.5-pro",
                        choices=["gemini-2.5-pro", "gemini-2.5-flash"],
                        help="Gemini model version (default: gemini-2.5-pro)")
    parser.add_argument("--extensions", "-e", nargs="+",
                        default=[".mp3", ".wav", ".flac", ".m4a", ".ogg"],
                        help="File extensions to process (default: .mp3 .wav .flac .m4a .ogg)")
    args = parser.parse_args()

    processor = GeminiProcessor(model_name=args.model)

    print(f"🎧 ASR Pipeline — Kabyle Audio Transcription")
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

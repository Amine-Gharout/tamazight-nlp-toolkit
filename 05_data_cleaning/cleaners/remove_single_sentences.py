"""
Remove lines without tabs (single sentences) from parallel corpus files.

A valid parallel pair must have source and target separated by a tab.
Lines without tabs are unpaired sentences that should be removed.

Usage:
    python cleaners/remove_single_sentences.py --input fr_kab.txt --output clean_fr_kab.txt
    python cleaners/remove_single_sentences.py --input fr_kab.txt --in-place
"""

import argparse
import os


def remove_single_sentences(input_file: str, output_file: str | None = None, in_place: bool = False):
    """
    Remove lines that don't contain a tab separator.

    Args:
        input_file: Path to input parallel corpus file.
        output_file: Path to output file (ignored if in_place=True).
        in_place: If True, overwrite input file (use with caution).
    """
    if not os.path.exists(input_file):
        print(f"❌ File not found: {input_file}")
        return

    with open(input_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    total = len(lines)
    cleaned = [line for line in lines if '\t' in line]
    removed = total - len(cleaned)

    if in_place:
        output_file = input_file
    elif output_file is None:
        stem, ext = os.path.splitext(input_file)
        output_file = f"{stem}_paired{ext}"

    with open(output_file, "w", encoding="utf-8") as f:
        f.writelines(cleaned)

    print(f"📄 Cleaning complete:")
    print(f"   Input:  {input_file}")
    print(f"   Total:  {total:,} lines")
    print(f"   Kept:   {len(cleaned):,} lines (with tab separator)")
    print(f"   Removed: {removed:,} lines (single/unpaired)")
    print(f"   Output: {output_file}")

    if removed > 0:
        print(f"\n⚠️  Sample removed lines (first 3):")
        shown = 0
        for line in lines:
            if '\t' not in line and line.strip() and shown < 3:
                print(f"   '{line.strip()[:80]}'")
                shown += 1


def main():
    parser = argparse.ArgumentParser(
        description="Remove single/unpaired sentences from parallel corpus")
    parser.add_argument("--input", "-i", required=True,
                        help="Input parallel corpus file")
    parser.add_argument("--output", "-o",
                        help="Output file path (default: input_paired.ext)")
    parser.add_argument("--in-place", action="store_true",
                        help="Overwrite input file directly")
    args = parser.parse_args()

    remove_single_sentences(args.input, args.output, args.in_place)


if __name__ == "__main__":
    main()

"""
Replace tab characters in parallel corpus files.

This handles dataset-specific tab formatting issues.
By default, it outputs to a new file to avoid data loss.

Usage:
    python cleaners/replace_tabs.py --input en_kab_pairs.txt --output clean_en_kab_pairs.txt
    python cleaners/replace_tabs.py --input en_kab_pairs.txt --in-place  # careful!
"""

import argparse
import os


def replace_tabs(input_file: str, output_file: str | None = None, in_place: bool = False):
    """
    Replace tabs in a parallel corpus file.

    Args:
        input_file: Path to input file.
        output_file: Path to output file (ignored if in_place=True).
        in_place: If True, overwrite the input file (use with caution).
    """
    if not os.path.exists(input_file):
        print(f"❌ File not found: {input_file}")
        return

    with open(input_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Count original tabs
    original_tabs = content.count("\t")

    # Perform the replacement
    # NOTE: Customize this logic for your specific dataset needs
    new_content = content.replace("\t", "\t\t\t\t")
    new_tabs = new_content.count("\t")

    if in_place:
        output_file = input_file
    elif output_file is None:
        stem, ext = os.path.splitext(input_file)
        output_file = f"{stem}_replaced{ext}"

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"📄 Tab replacement complete:")
    print(f"   Input:  {input_file}")
    print(f"   Output: {output_file}")
    print(
        f"   Tabs:   {original_tabs:,} → {new_tabs:,} ({new_tabs - original_tabs:,} added)")
    print(
        f"   Size:   {os.path.getsize(input_file):,} → {os.path.getsize(output_file):,} bytes")


def main():
    parser = argparse.ArgumentParser(
        description="Replace tabs in parallel corpus files")
    parser.add_argument("--input", "-i", required=True,
                        help="Input file path")
    parser.add_argument("--output", "-o",
                        help="Output file path (default: input_replaced.ext)")
    parser.add_argument("--in-place", action="store_true",
                        help="Overwrite input file directly (use with caution!)")
    args = parser.parse_args()

    replace_tabs(args.input, args.output, in_place=args.in_place)


if __name__ == "__main__":
    main()

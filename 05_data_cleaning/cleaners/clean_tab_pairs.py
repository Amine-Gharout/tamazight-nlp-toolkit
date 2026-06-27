"""
Programme pour nettoyer un fichier de paires (français/kabyle).
Garde uniquement les lignes qui contiennent un tab (séparateur valide).

Usage:
    python cleaners/clean_tab_pairs.py --input fra_kab_pairs.txt --output clean_fra_kab_pairs.txt
    python cleaners/clean_tab_pairs.py --input fra_kab_pairs.txt --in-place
"""

import argparse
import os


def clean_tab_pairs(input_file: str, output_file: str | None = None, in_place: bool = False):
    """
    Keep only lines containing a tab (valid separator).

    Args:
        input_file: Input file path.
        output_file: Output file path (ignored if in_place=True).
        in_place: If True, overwrite input file directly.
    """
    if not os.path.exists(input_file):
        print(f" File not found: {input_file}")
        return

    total_lines = 0
    kept_lines = 0
    removed_lines = 0

    valid_lines = []
    invalid_lines = []

    print(f" Reading: {input_file}")

    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            total_lines += 1
            if '\t' in line:
                valid_lines.append(line)
                kept_lines += 1
            else:
                removed_lines += 1
                if line.strip():
                    invalid_lines.append((total_lines, line.strip()[:80]))

    if in_place:
        output_file = input_file
    elif output_file is None:
        stem, ext = os.path.splitext(input_file)
        output_file = f"{stem}_clean{ext}"

    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(valid_lines)

    print(f"\n{'='*60}")
    print("CLEANUP SUMMARY")
    print(f"{'='*60}")
    print(f"   Total lines:     {total_lines:,}")
    print(f"   Kept (with tab): {kept_lines:,}")
    print(f"   Removed (no tab): {removed_lines:,}")
    print(f"   Output: {output_file}")
    print(f"{'='*60}")

    if invalid_lines:
        print(f"\n Sample removed lines (max 5):")
        for line_num, content in invalid_lines[:5]:
            print(f"   Line {line_num}: '{content}...'")

    print(f"\n Done: {output_file}")


def main():
    parser = argparse.ArgumentParser(
        description="Clean parallel corpus files by keeping only tab-separated lines")
    parser.add_argument("--input", "-i", required=True,
                        help="Input parallel corpus file")
    parser.add_argument("--output", "-o",
                        help="Output file path (default: input_clean.ext)")
    parser.add_argument("--in-place", action="store_true",
                        help="Overwrite input file directly")
    args = parser.parse_args()

    clean_tab_pairs(args.input, args.output, args.in_place)


if __name__ == "__main__":
    main()

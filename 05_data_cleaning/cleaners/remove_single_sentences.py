input_file = "fr_kab.txt"
output_file = input_file

with open(input_file, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Keep only lines that have at least one tab (meaning they have two sentences)
cleaned_lines = [line for line in lines if '\t' in line]

removed_count = len(lines) - len(cleaned_lines)

with open(output_file, "w", encoding="utf-8") as f:
    f.writelines(cleaned_lines)

print(f"Removed {removed_count} lines with single sentences.")
print(f"Kept {len(cleaned_lines)} lines. Saved to {output_file}")

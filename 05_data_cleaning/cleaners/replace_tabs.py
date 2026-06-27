input_file = "en_kab_pairs.txt"
output_file = input_file

with open(input_file, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("\t", "\t\t\t\t")

with open(output_file, "w", encoding="utf-8") as f:
    f.write(content)

print(f"Replaced double tabs with triple tabs. Saved to {output_file}")

"""
Programme pour nettoyer un fichier de paires (français/kabyle).
Garde uniquement les lignes qui contiennent un tab (séparateur valide).
"""

# ============================================
# CONFIGURATION
# ============================================
INPUT_FILE = "fra_kab_pairs.txt"
OUTPUT_FILE = "clean_fra_kab_pairs.txt"
# ============================================


def clean_tab_pairs(input_file: str, output_file: str):
    """
    Garde uniquement les lignes contenant un tab (séparateur valide).
    Les lignes sans tab sont considérées comme corrompues/mal formées.

    Args:
        input_file: Fichier d'entrée
        output_file: Fichier de sortie nettoyé
    """
    total_lines = 0
    kept_lines = 0
    removed_lines = 0

    valid_lines = []
    invalid_lines = []

    print(f"📂 Lecture du fichier: {input_file}")

    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            total_lines += 1

            # Vérifier si la ligne contient un tab (séparateur valide)
            if '\t' in line:
                valid_lines.append(line)
                kept_lines += 1
            else:
                removed_lines += 1
                # Garder trace des lignes invalides pour inspection
                if line.strip():  # Ignorer les lignes vides
                    invalid_lines.append((total_lines, line.strip()[:80]))

    # Sauvegarder les lignes valides
    print(f"\n💾 Sauvegarde vers: {output_file}")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(valid_lines)

    # Afficher le résumé
    print(f"\n{'='*60}")
    print(f"RÉSUMÉ DU NETTOYAGE")
    print(f"{'='*60}")
    print(f"   Lignes totales:     {total_lines:,}")
    print(f"   Lignes gardées:     {kept_lines:,} (avec tab)")
    print(f"   Lignes supprimées:  {removed_lines:,} (sans tab)")
    print(f"{'='*60}")

    # Afficher quelques lignes invalides pour inspection
    if invalid_lines:
        print(f"\n⚠️ Exemples de lignes supprimées (max 10):")
        for line_num, content in invalid_lines[:10]:
            print(f"   Ligne {line_num}: '{content}...'")

    print(f"\n✅ Fichier nettoyé sauvegardé: {output_file}")

    return kept_lines, removed_lines


if __name__ == "__main__":
    clean_tab_pairs(INPUT_FILE, OUTPUT_FILE)

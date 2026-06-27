#!/usr/bin/env bash
#
# download_data.sh — Download raw datasets from Google Drive
#
# Usage:
#   bash scripts/download_data.sh
#
# Downloads ~619 MB of raw parallel corpora (11 files) to 0_data/raw/.
# Uses gdown to pull files from a shared Google Drive folder.
# DVC-tracked so you can verify integrity with `dvc checkout`.
#
# Prerequisites:
#   pip install gdown    (installed automatically if missing)
#   dvc                  (for verification, optional)
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
DATA_DIR="$PROJECT_ROOT/0_data"
RAW_DIR="$DATA_DIR/raw"

# ══════════════════════════════════════════════════════════
# CONFIG — Google Drive folder link
# ──────────────────────────────────────────────────────────
# Replace with your own link if hosting the data yourself.
# The folder must be shared with "Anyone with the link" access.
# ══════════════════════════════════════════════════════════
GDRIVE_LINK="https://drive.google.com/drive/folders/1_FC0n1Jx6pzhVVnMLAVzO4rRxCdayrh-?usp=sharing"

# ─── Extract folder ID from URL ───
if [[ "$GDRIVE_LINK" =~ /folders/([^/?]+) ]]; then
    GDRIVE_FOLDER_ID="${BASH_REMATCH[1]}"
else
    echo "❌ ERROR: Invalid Google Drive URL. Expected a folder link (containing /folders/...)"
    echo "   Got: $GDRIVE_LINK"
    exit 1
fi

echo "╔══════════════════════════════════════════════════════════╗"
echo "║       chat_aqvayli — Raw Data Downloader               ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""
echo "  Google Drive folder: ${GDRIVE_FOLDER_ID}"
echo "  Target directory:    ${RAW_DIR}"
echo "  Expected size:       ~619 MB (11 files)"
echo ""

# ─── Skip if data already present ───
if [ -d "$RAW_DIR" ] && [ "$(ls -A "$RAW_DIR" 2>/dev/null)" ]; then
    FILE_COUNT=$(find "$RAW_DIR" -type f | wc -l)
    TOTAL_SIZE=$(du -sh "$RAW_DIR" | cut -f1)
    echo "✅ Data already exists at ${RAW_DIR}/"
    echo "   Files: ${FILE_COUNT} | Size: ${TOTAL_SIZE}"
    echo ""
    echo "   To re-download, first remove it:"
    echo "     rm -rf ${RAW_DIR}"
    echo "   Then run this script again."
    exit 0
fi

# ─── Install gdown if missing ───
if ! python -c "import gdown" 2>/dev/null; then
    echo "📦 Installing gdown (Google Drive downloader)..."
    pip install gdown
    echo ""
fi

# ─── Download entire folder via gdown ───
echo "⬇️  Downloading from Google Drive..."
echo "   (This may take a few minutes depending on your connection)"
echo ""

mkdir -p "$RAW_DIR"

python -c "
import gdown, os, zipfile, tarfile, glob

folder_id = '$GDRIVE_FOLDER_ID'
output_dir = '$RAW_DIR'

files = gdown.download_folder(id=folder_id, output=output_dir, quiet=False)

if not files:
    print()
    print('❌ ERROR: No files downloaded.')
    print('   Possible reasons:')
    print('   1. The folder is not shared publicly (set to \"Anyone with the link\")')
    print('   2. The folder ID is wrong or the folder is empty')
    print('   3. Google Drive rate-limited — wait a few minutes and retry')
    exit(1)

print()
print(f'✅ Downloaded {len(files)} files:')
for f in sorted(files):
    size_mb = os.path.getsize(f) / (1024 * 1024)
    print(f'   {os.path.basename(f):40s} {size_mb:8.1f} MB')

# Extract archives if any were downloaded
for f in files:
    if f.endswith('.zip'):
        print(f'\n📦 Extracting {os.path.basename(f)}...')
        with zipfile.ZipFile(f, 'r') as zf:
            zf.extractall(output_dir)
        os.remove(f)
        print('   Done — zip removed.')
        break
    elif f.endswith(('.tar.gz', '.tgz')):
        print(f'\n📦 Extracting {os.path.basename(f)}...')
        with tarfile.open(f, 'r:gz') as tf:
            tf.extractall(output_dir)
        os.remove(f)
        print('   Done — archive removed.')
        break
"

# ─── Summary ───
TOTAL=$(du -sh "$RAW_DIR" | cut -f1)
FILE_COUNT=$(find "$RAW_DIR" -type f | wc -l)
echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║  ✅ Download complete!                                  ║"
echo "║  Target: ${RAW_DIR}"
echo "║  Files:  ${FILE_COUNT} | Size: ${TOTAL}"
echo "╚══════════════════════════════════════════════════════════╝"

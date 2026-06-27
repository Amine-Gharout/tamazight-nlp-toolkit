#!/usr/bin/env bash
#
# download_data.sh — Download raw datasets from Google Drive
#
# Usage:
#   bash scripts/download_data.sh
#
# Downloads ~619 MB of raw parallel corpora to 0_data/raw/.
# The data is on Google Drive as a single raw_data.tar.gz archive.
# Uses gdown to download the file, then extracts it into 0_data/raw/.
#
# Prerequisites:
#   pip install gdown    (installed automatically if missing)
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
DATA_DIR="$PROJECT_ROOT/0_data"
RAW_DIR="$DATA_DIR/raw"

# ══════════════════════════════════════════════════════════
# CONFIG — Google Drive file ID of raw_data.tar.gz
# ──────────────────────────────────────────────────────────
# The data is packaged as a single .tar.gz archive on Google Drive.
# The file must be shared with "Anyone with the link" access.
# ══════════════════════════════════════════════════════════
GDRIVE_FILE_ID="1lpl1N3MXPk8ZrnIyAqb_WNLBx5CJ_kbH"

echo "╔══════════════════════════════════════════════════════════╗"
echo "║       chat_aqvayli — Raw Data Downloader               ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""
echo "  Google Drive file ID: ${GDRIVE_FILE_ID}"
echo "  Target directory:     ${RAW_DIR}"
echo "  Expected size:        ~619 MB (11 files in .tar.gz)"
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

# ─── Download the .tar.gz file ───
ARCHIVE="$DATA_DIR/raw_data.tar.gz"
echo "⬇️  Downloading raw_data.tar.gz from Google Drive..."
echo "   (This may take a few minutes depending on your connection)"
echo ""

python -c "
import gdown, os, sys

file_id = '$GDRIVE_FILE_ID'
output = '$ARCHIVE'

print(f'Downloading file {file_id}...')
gdown.download(id=file_id, output=output, quiet=False)

if not os.path.exists(output) or os.path.getsize(output) < 10000:
    print()
    print('❌ ERROR: Download failed or file too small.')
    print('   Possible reasons:')
    print('   1. The file is not shared publicly (set to \"Anyone with the link\")')
    print('   2. The file ID is wrong')
    print('   3. Google Drive rate-limited — wait a few minutes and retry')
    sys.exit(1)

size_mb = os.path.getsize(output) / (1024 * 1024)
print(f'✅ Downloaded: {size_mb:.1f} MB')
"

# ─── Extract the archive ───
echo ""
echo "📦 Extracting raw_data.tar.gz to ${RAW_DIR}/..."
mkdir -p "$RAW_DIR"
tar xzf "$ARCHIVE" -C "$DATA_DIR"
rm "$ARCHIVE"
echo "   Done — archive removed."

# ─── Summary ───
TOTAL=$(du -sh "$RAW_DIR" | cut -f1)
FILE_COUNT=$(find "$RAW_DIR" -type f | wc -l)
echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║  ✅ Download complete!                                  ║"
echo "║  Target: ${RAW_DIR}"
echo "║  Files:  ${FILE_COUNT} | Size: ${TOTAL}"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║  ✅ Download complete!                                  ║"
echo "║  Target: ${RAW_DIR}"
echo "║  Files:  ${FILE_COUNT} | Size: ${TOTAL}"
echo "╚══════════════════════════════════════════════════════════╝"

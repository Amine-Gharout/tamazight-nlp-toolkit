#!/usr/bin/env bash
#
# download_data.sh — Download raw datasets from Google Drive
#
# Usage:
#   bash scripts/download_data.sh
#
# This downloads the raw data files to 0_data/raw/
# The data is hosted on Google Drive as a shared folder.
#
# Prerequisites:
#   pip install gdown
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
DATA_DIR="$PROJECT_ROOT/0_data"
RAW_DIR="$DATA_DIR/raw"

# ═══════════════════════════════════════════════════════
# CONFIG: Paste your Google Drive folder link below
# ═══════════════════════════════════════════════════════
GDRIVE_LINK="https://drive.google.com/drive/folders/1_FC0n1Jx6pzhVVnMLAVzO4rRxCdayrh-?usp=sharing"

# Extract folder ID from URL
if [[ "$GDRIVE_LINK" =~ /folders/([^/?]+) ]]; then
    GDRIVE_FOLDER_ID="${BASH_REMATCH[1]}"
elif [[ "$GDRIVE_LINK" =~ /d/([^/?]+) ]]; then
    # It's a file URL, not a folder
    echo "ERROR: This looks like a file URL, not a folder URL."
    echo "Please provide a Google Drive folder link (containing /folders/...)"
    exit 1
else
    GDRIVE_FOLDER_ID="$GDRIVE_LINK"
fi

if [ -z "$GDRIVE_FOLDER_ID" ] || [ "$GDRIVE_FOLDER_ID" = "YOUR_FOLDER_ID_HERE" ]; then
    echo "ERROR: You must set a valid Google Drive folder link in this script."
    echo ""
    echo "Steps:"
    echo "  1. Upload your data files to a Google Drive folder"
    echo "  2. Share the folder (anyone with link can view)"
    echo "  3. Paste the folder link into this script"
    exit 1
fi

echo "Downloading raw data from Google Drive folder..."
echo "Folder ID: $GDRIVE_FOLDER_ID"
echo "Target:    $RAW_DIR"
echo ""

# Check if data already exists
if [ -d "$RAW_DIR" ] && [ "$(ls -A "$RAW_DIR" 2>/dev/null)" ]; then
    echo "Data already exists at $RAW_DIR/"
    echo "Remove it first if you want to re-download: rm -rf $RAW_DIR/"
    exit 0
fi

# Install gdown if not present
if ! python -c "import gdown" 2>/dev/null; then
    echo "Installing gdown..."
    pip install gdown
fi

# Download entire folder
mkdir -p "$RAW_DIR"
python -c "
import gdown, os, zipfile, shutil, glob

folder_id = '$GDRIVE_FOLDER_ID'
output_dir = '$RAW_DIR'

print(f'Downloading folder {folder_id} to {output_dir}...')
files = gdown.download_folder(id=folder_id, output=output_dir, quiet=False)

if not files:
    print('WARNING: No files downloaded. The folder may be empty or not shared publicly.')
    exit(1)

print(f'\nDownloaded {len(files)} files:')
for f in files:
    size_mb = os.path.getsize(f) / (1024 * 1024)
    print(f'  {os.path.basename(f)}: {size_mb:.1f} MB')

# If a zip file was downloaded, extract it
for f in files:
    if f.endswith('.zip'):
        print(f'\nExtracting {os.path.basename(f)}...')
        with zipfile.ZipFile(f, 'r') as zf:
            zf.extractall(output_dir)
        os.remove(f)
        print('Extraction complete. Zip file removed.')
        break
    elif f.endswith('.tar.gz') or f.endswith('.tgz'):
        import tarfile
        print(f'\nExtracting {os.path.basename(f)}...')
        with tarfile.open(f, 'r:gz') as tf:
            tf.extractall(output_dir)
        os.remove(f)
        print('Extraction complete. Archive removed.')
        break
"

echo ""
echo "Done! Data downloaded to $RAW_DIR/"
echo ""
echo "Verifying with DVC..."
cd "$PROJECT_ROOT" && dvc checkout 2>/dev/null || true
echo "Data is ready."

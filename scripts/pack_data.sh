#!/usr/bin/env bash
#
# pack_data.sh — Instructions for uploading raw data to Google Drive
#
# The data is uploaded as individual files to a Google Drive folder.
# No archiving needed — just upload the 0_data/raw/ folder contents directly.
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
DATA_DIR="$PROJECT_ROOT/0_data/raw"

if [ ! -d "$DATA_DIR" ]; then
    echo "ERROR: $DATA_DIR not found. Nothing to upload."
    exit 1
fi

echo "Files to upload from $DATA_DIR:"
echo ""
du -h "$DATA_DIR"/* 2>/dev/null || true
echo ""

TOTAL=$(du -sh "$DATA_DIR" | cut -f1)
echo "Total size: $TOTAL"
echo ""
echo "Next steps:"
echo "  1. Go to https://drive.google.com"
echo "  2. Create a new folder (e.g., 'chat_aqvayli_data')"
echo "  3. Upload ALL files from $DATA_DIR into that folder"
echo "  4. Share the folder: Right-click → Share → 'Anyone with the link'"
echo "  5. Copy the folder link (looks like: /drive/folders/...)"
echo "  6. Paste it into scripts/download_data.sh"

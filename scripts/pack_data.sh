#!/usr/bin/env bash
#
# pack_data.sh — Package raw data into a .tar.gz archive for Google Drive
#
# Creates raw_data.tar.gz from the 0_data/raw/ directory contents,
# ready to upload to Google Drive for sharing.
#
# Usage:
#   bash scripts/pack_data.sh
#
# Then upload the generated raw_data.tar.gz to Google Drive,
# copy the file ID, and paste it into scripts/download_data.sh.
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
DATA_DIR="$PROJECT_ROOT/0_data"
RAW_DIR="$DATA_DIR/raw"
ARCHIVE="$DATA_DIR/raw_data.tar.gz"

if [ ! -d "$RAW_DIR" ]; then
    echo "❌ ERROR: $RAW_DIR not found."
    echo "   Make sure you have the raw data files in 0_data/raw/ before running this script."
    exit 1
fi

if [ -z "$(ls -A "$RAW_DIR" 2>/dev/null)" ]; then
    echo "❌ ERROR: $RAW_DIR is empty. Nothing to pack."
    exit 1
fi

echo "╔══════════════════════════════════════════════════════════╗"
echo "║       chat_aqvayli — Data Archiver                     ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Show files to pack
echo "📁 Files to archive from $RAW_DIR:"
echo ""
FILE_COUNT=$(find "$RAW_DIR" -type f | wc -l)
TOTAL_SIZE=$(du -sh "$RAW_DIR" | cut -f1)
du -h "$RAW_DIR"/* 2>/dev/null || true
echo ""
echo "   Total: ${FILE_COUNT} files, ${TOTAL_SIZE}"

# Create archive
echo ""
echo "📦 Creating archive: ${ARCHIVE}"
tar czf "$ARCHIVE" -C "$DATA_DIR" raw

ARCHIVE_SIZE=$(du -h "$ARCHIVE" | cut -f1)
echo "   ✅ Created: ${ARCHIVE} (${ARCHIVE_SIZE})"
echo ""

# Instructions
echo "╔══════════════════════════════════════════════════════════╗"
echo "║  Next steps:                                           ║"
echo "║  1. Upload ${ARCHIVE} to Google Drive              ║"
echo "║  2. Share the file → \"Anyone with the link\"            ║"
echo "║  3. Copy the file ID from the share URL                 ║"
echo "║     (the long string between /d/ and /view)             ║"
echo "║  4. Paste it into scripts/download_data.sh              ║"
echo "║     at: GDRIVE_FILE_ID=\"your-file-id-here\"              ║"
echo "╚══════════════════════════════════════════════════════════╝"

#!/bin/bash
# Azure VM Startup Script for Radio Recording Service
# Runs on boot: records Radio Chaine 2 and uploads to Azure Blob Storage

echo "=========================================="
echo " Starting Radio Recording Service"
echo "=========================================="

# Verify Python
echo "Python version: $(python --version)"

# Install Python dependencies
echo "Installing Python packages..."
pip install --upgrade pip
pip install azure-storage-blob imageio-ffmpeg

# Environment variables (set these in Azure Portal → VM → Environment)
# AZURE_STORAGE_CONNECTION_STRING — required for Blob Storage upload
# CONTAINER_NAME — defaults to "recordings"

if [ -z "$AZURE_STORAGE_CONNECTION_STRING" ]; then
    echo "WARNING: AZURE_STORAGE_CONNECTION_STRING is not set."
    echo "Set it in Azure Portal or add to /etc/environment"
fi

echo "Starting radio recorder..."
echo "=========================================="

cd "$(dirname "$0")"
python -u radio_recorder_azure_vm.py

echo "Service stopped"

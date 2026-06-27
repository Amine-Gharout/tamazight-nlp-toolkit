#!/bin/bash
# Azure Web App Startup Script for Radio Recording Service

echo "=========================================="
echo "🚀 Starting Radio Recording Service"
echo "=========================================="

# Verify Python
echo "🐍 Python version: $(python --version)"

# Install Python dependencies
echo "📚 Installing Python packages..."
pip install --upgrade pip
pip install -r requirements_webapp.txt

# Set environment variables (these should be configured in Azure Portal)
# AZURE_STORAGE_CONNECTION_STRING should be set in Azure App Configuration

# Run the radio recording service with Flask
echo "🎙️  Starting radio recording service..."
echo "=========================================="

# Run with unbuffered output and use gunicorn for production
echo "Starting Flask application..."
python -u azure_radio_app.py

echo "⏹️  Service stopped"

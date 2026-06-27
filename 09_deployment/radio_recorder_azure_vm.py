#!/usr/bin/env python3
"""
Radio Chaine 2 Continuous Recorder for Azure
Records live radio stream and uploads to Azure Blob Storage
"""

import subprocess
import os
from datetime import datetime
import time
from azure.storage.blob import BlobServiceClient
import tempfile
import sys

# Configuration
STREAM_URL = "https://radiochaine2.ice.infomaniak.ch/chaine2.mp3"
CHUNK_DURATION = 300  # 5 minutes in seconds

# Azure Storage Configuration
AZURE_STORAGE_CONNECTION_STRING = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
CONTAINER_NAME = os.getenv('CONTAINER_NAME', 'recordings')

# Validate configuration
if not AZURE_STORAGE_CONNECTION_STRING:
    print("❌ ERROR: AZURE_STORAGE_CONNECTION_STRING environment variable is required")
    sys.exit(1)

# Initialize Azure Blob Storage
try:
    blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
    container_client = blob_service_client.get_container_client(CONTAINER_NAME)
    
    # Create container if it doesn't exist
    if not container_client.exists():
        container_client.create_container()
        print(f"✅ Created Azure Blob container: {CONTAINER_NAME}")
except Exception as e:
    print(f"❌ ERROR: Failed to initialize Azure Blob Storage: {e}")
    sys.exit(1)

print("="*60)
print("🎙️  LIVE RADIO RECORDING - Azure Blob Storage")
print("="*60)
print(f"📻 Stream URL: {STREAM_URL}")
print(f"⏱️  Chunk Duration: {CHUNK_DURATION} seconds ({CHUNK_DURATION//60} minutes)")
print(f"☁️  Azure Container: {CONTAINER_NAME}")
print(f"🕐 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*60)
print("\n🔄 Running continuously...\n")

chunk_counter = 1

def record_and_upload():
    """Record one chunk and upload to Azure"""
    global chunk_counter
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    temp_file = os.path.join(tempfile.gettempdir(), f"radio_temp_{timestamp}.mp3")
    blob_name = f"radio_chaine2_{timestamp}_chunk{chunk_counter}.mp3"
    
    print(f"\n{'='*60}")
    print(f"🎬 Recording Chunk #{chunk_counter}")
    print(f"🕐 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}")
    
    try:
        # Record using ffmpeg
        from imageio_ffmpeg import get_ffmpeg_exe
        ffmpeg_path = get_ffmpeg_exe()
        
        cmd = [
            ffmpeg_path,
            "-i", STREAM_URL,
            "-t", str(CHUNK_DURATION),
            "-acodec", "libmp3lame",
            "-ab", "128k",
            "-y",
            temp_file
        ]
        
        print(f"📡 Recording to temporary file...")
        result = subprocess.run(cmd, capture_output=True, timeout=CHUNK_DURATION + 30, text=True)
        
        if os.path.exists(temp_file) and os.path.getsize(temp_file) > 10000:
            file_size = os.path.getsize(temp_file) / (1024 * 1024)
            
            # Upload to Azure Blob Storage
            print(f"☁️  Uploading to Azure Blob Storage...")
            blob_client = blob_service_client.get_blob_client(
                container=CONTAINER_NAME, 
                blob=blob_name
            )
            
            with open(temp_file, "rb") as data:
                blob_client.upload_blob(data, overwrite=True)
            
            print(f"\n✅ Successfully uploaded chunk #{chunk_counter}")
            print(f"📦 Blob: {blob_name}")
            print(f"💾 Size: {file_size:.2f} MB")
            
            # Clean up temporary file
            os.remove(temp_file)
            return True
            
        else:
            print(f"\n❌ Recording failed - file too small or missing")
            if os.path.exists(temp_file):
                os.remove(temp_file)
            return False
            
    except subprocess.TimeoutExpired:
        if os.path.exists(temp_file) and os.path.getsize(temp_file) > 10000:
            file_size = os.path.getsize(temp_file) / (1024 * 1024)
            
            # Upload even if timeout
            print(f"☁️  Uploading (timeout but valid file)...")
            blob_client = blob_service_client.get_blob_client(
                container=CONTAINER_NAME,
                blob=blob_name
            )
            
            with open(temp_file, "rb") as data:
                blob_client.upload_blob(data, overwrite=True)
            
            print(f"\n✅ Uploaded (with timeout)")
            print(f"📦 Blob: {blob_name}")
            print(f"💾 Size: {file_size:.2f} MB")
            
            os.remove(temp_file)
            return True
        else:
            print(f"\n❌ Recording timeout - file incomplete")
            if os.path.exists(temp_file):
                os.remove(temp_file)
            return False
            
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        if os.path.exists(temp_file):
            os.remove(temp_file)
        return False

# Main loop
try:
    while True:
        record_and_upload()
        chunk_counter += 1
        
        # Small delay between chunks
        print(f"\n⏸️  Waiting 2 seconds before next chunk...")
        time.sleep(2)
        
except KeyboardInterrupt:
    print("\n\n" + "="*60)
    print("⏹️  Recording stopped")
    print(f"📊 Total chunks recorded: {chunk_counter - 1}")
    print(f"☁️  Files saved in Azure Blob: {CONTAINER_NAME}")
    print("="*60)
except Exception as e:
    print(f"\n\n❌ FATAL ERROR: {str(e)}")
    sys.exit(1)

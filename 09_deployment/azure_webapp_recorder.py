#!/usr/bin/env python3
"""
Azure Web App Radio Recording & Transcription Service
Records live radio stream and uploads to Azure Blob Storage
"""

import subprocess
import os
from datetime import datetime
import time
from azure.storage.blob import BlobServiceClient
import tempfile
import sys
import threading
from flask import Flask, jsonify

# ============= CONFIGURATION =============
STREAM_URL = "https://radiochaine2.ice.infomaniak.ch/chaine2.mp3"
CHUNK_DURATION = 300  # 5 minutes in seconds

# Azure Storage Configuration - READ FROM ENVIRONMENT
AZURE_STORAGE_CONNECTION_STRING = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
if not AZURE_STORAGE_CONNECTION_STRING:
    raise ValueError("❌ AZURE_STORAGE_CONNECTION_STRING environment variable not set!")

CONTAINER_NAME = "recordings"  # Blob container for audio files

# ============= AZURE BLOB SETUP =============
print("🔧 Initializing Azure Blob Storage client...")
blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)

# Ensure container exists
try:
    container_client = blob_service_client.get_container_client(CONTAINER_NAME)
    if not container_client.exists():
        container_client.create_container()
        print(f"✅ Created Azure Blob container: {CONTAINER_NAME}")
    else:
        print(f"✅ Azure Blob container ready: {CONTAINER_NAME}")
except Exception as e:
    print(f"⚠️  Container initialization: {e}")

# ============= LOGGING SETUP =============
def log(message):
    """Timestamped logging"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}", flush=True)

# ============= MAIN RECORDING FUNCTION =============
def record_and_upload_chunk(chunk_counter):
    """Record a chunk of stream and upload to Azure Blob Storage"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    temp_file = os.path.join(tempfile.gettempdir(), f"radio_temp_{timestamp}.mp3")
    blob_name = f"radio_chaine2_{timestamp}_chunk{chunk_counter}.mp3"
    
    log(f"{'='*60}")
    log(f"🎬 Recording Chunk #{chunk_counter}")
    log(f"{'='*60}")
    
    try:
        # Import ffmpeg
        try:
            from imageio_ffmpeg import get_ffmpeg_exe
            ffmpeg_path = get_ffmpeg_exe()
        except ImportError:
            # Fallback to system ffmpeg
            ffmpeg_path = "ffmpeg"
            log("⚠️  Using system ffmpeg (imageio-ffmpeg not available)")
        
        # Build ffmpeg command
        cmd = [
            ffmpeg_path,
            "-i", STREAM_URL,
            "-t", str(CHUNK_DURATION),
            "-acodec", "libmp3lame",
            "-ab", "128k",
            "-y",
            temp_file
        ]
        
        log(f"📡 Recording to temporary file...")
        result = subprocess.run(
            cmd, 
            capture_output=True, 
            timeout=CHUNK_DURATION + 60,
            text=True
        )
        
        # Check if recording was successful
        if os.path.exists(temp_file) and os.path.getsize(temp_file) > 10000:
            file_size = os.path.getsize(temp_file) / (1024 * 1024)
            log(f"✅ Recording complete: {file_size:.2f} MB")
            
            # Upload to Azure Blob Storage
            log(f"☁️  Uploading to Azure Blob Storage...")
            blob_client = blob_service_client.get_blob_client(
                container=CONTAINER_NAME, 
                blob=blob_name
            )
            
            with open(temp_file, "rb") as data:
                blob_client.upload_blob(data, overwrite=True)
            
            log(f"✅ Successfully uploaded chunk #{chunk_counter}")
            log(f"📦 Blob: {blob_name}")
            log(f"💾 Size: {file_size:.2f} MB")
            
            # Clean up temporary file
            os.remove(temp_file)
            log(f"🗑️  Cleaned up temporary file")
            
            return True
            
        else:
            log(f"❌ Recording failed - file too small or missing")
            if os.path.exists(temp_file):
                os.remove(temp_file)
            return False
                
    except subprocess.TimeoutExpired:
        log(f"⚠️  Recording timeout after {CHUNK_DURATION + 60}s")
        
        # Try to upload anyway if file exists
        if os.path.exists(temp_file) and os.path.getsize(temp_file) > 10000:
            try:
                file_size = os.path.getsize(temp_file) / (1024 * 1024)
                log(f"☁️  Uploading partial recording...")
                
                blob_client = blob_service_client.get_blob_client(
                    container=CONTAINER_NAME,
                    blob=blob_name
                )
                
                with open(temp_file, "rb") as data:
                    blob_client.upload_blob(data, overwrite=True)
                
                log(f"✅ Uploaded partial chunk: {file_size:.2f} MB")
                os.remove(temp_file)
                return True
            except Exception as upload_error:
                log(f"❌ Upload failed: {upload_error}")
                if os.path.exists(temp_file):
                    os.remove(temp_file)
                return False
        else:
            log(f"❌ Recording timeout - file incomplete")
            if os.path.exists(temp_file):
                os.remove(temp_file)
            return False
            
    except Exception as e:
        log(f"❌ Error: {str(e)}")
        if os.path.exists(temp_file):
            try:
                os.remove(temp_file)
            except:
                pass
        return False

# ============= MAIN LOOP =============
# Global status tracking
recording_status = {
    "is_running": False,
    "chunks_recorded": 0,
    "last_chunk_time": None,
    "last_error": None,
    "uptime_start": None
}

# Flask app for health checks
app = Flask(__name__)

@app.route('/')
def index():
    """Health check endpoint"""
    return jsonify({
        "status": "running",
        "service": "Radio Recording Service",
        "chunks_recorded": recording_status["chunks_recorded"],
        "last_chunk": recording_status["last_chunk_time"],
        "is_recording": recording_status["is_running"],
        "uptime_start": recording_status["uptime_start"],
        "error": recording_status["last_error"]
    })

@app.route('/health')
def health():
    """Simple health check"""
    return "OK", 200

def recording_loop():
    """Background thread for continuous recording"""
    recording_status["uptime_start"] = datetime.now().isoformat()
    
    log("="*60)
    log("🎙️  AZURE RADIO RECORDING SERVICE")
    log("="*60)
    log(f"📻 Stream URL: {STREAM_URL}")
    log(f"⏱️  Chunk Duration: {CHUNK_DURATION}s ({CHUNK_DURATION//60} min)")
    log(f"☁️  Azure Container: {CONTAINER_NAME}")
    log(f"🐍 Python: {sys.version.split()[0]}")
    log("="*60)
    log("🔄 Starting continuous recording...\n")
    
    chunk_counter = 1
    consecutive_failures = 0
    max_consecutive_failures = 5
    
    try:
        while True:
            success = record_and_upload_chunk(chunk_counter)
            
            if success:
                consecutive_failures = 0
                chunk_counter += 1
                log(f"⏸️  Waiting 10 seconds before next chunk...\n")
                time.sleep(10)
            else:
                consecutive_failures += 1
                log(f"⚠️  Failure count: {consecutive_failures}/{max_consecutive_failures}")
                
                if consecutive_failures >= max_consecutive_failures:
                    log(f"❌ Too many consecutive failures ({consecutive_failures}). Exiting.")
                    break
                
                # Wait longer on failure
                log(f"⏸️  Waiting 30 seconds before retry...\n")
                time.sleep(30)
            
    except KeyboardInterrupt:
        log("\n⏹️  Recording stopped by user")
    except Exception as e:
        log(f"\n❌ Fatal error: {str(e)}")
        raise
    finally:
        log(f"📊 Total chunks recorded: {chunk_counter - 1}")
        log(f"☁️  All files saved in Azure Blob: {CONTAINER_NAME}")
        log("="*60)

def recording_loop():
    """Background thread for continuous recording"""
    recording_status["uptime_start"] = datetime.now().isoformat()
    
    log("="*60)
    log("🎙️  AZURE RADIO RECORDING SERVICE")
    log("="*60)
    log(f"📻 Stream URL: {STREAM_URL}")
    log(f"⏱️  Chunk Duration: {CHUNK_DURATION}s ({CHUNK_DURATION//60} min)")
    log(f"☁️  Azure Container: {CONTAINER_NAME}")
    log(f"🐍 Python: {sys.version.split()[0]}")
    log("="*60)
    log("🔄 Starting continuous recording...\n")
    
    chunk_counter = 1
    consecutive_failures = 0
    max_consecutive_failures = 5
    
    try:
        recording_status["is_running"] = True
        while True:
            success = record_and_upload_chunk(chunk_counter)
            
            if success:
                consecutive_failures = 0
                recording_status["chunks_recorded"] = chunk_counter
                recording_status["last_chunk_time"] = datetime.now().isoformat()
                recording_status["last_error"] = None
                chunk_counter += 1
                log(f"⏸️  Waiting 10 seconds before next chunk...\n")
                time.sleep(10)
            else:
                consecutive_failures += 1
                recording_status["last_error"] = f"Failed {consecutive_failures} times"
                log(f"⚠️  Failure count: {consecutive_failures}/{max_consecutive_failures}")
                
                if consecutive_failures >= max_consecutive_failures:
                    log(f"❌ Too many consecutive failures ({consecutive_failures}). Exiting.")
                    recording_status["is_running"] = False
                    break
                
                # Wait longer on failure
                log(f"⏸️  Waiting 30 seconds before retry...\n")
                time.sleep(30)
            
    except KeyboardInterrupt:
        log("\n⏹️  Recording stopped by user")
        recording_status["is_running"] = False
    except Exception as e:
        log(f"\n❌ Fatal error: {str(e)}")
        recording_status["last_error"] = str(e)
        recording_status["is_running"] = False
    finally:
        log(f"📊 Total chunks recorded: {chunk_counter - 1}")
        log(f"☁️  All files saved in Azure Blob: {CONTAINER_NAME}")
        log("="*60)

if __name__ == "__main__":
    # Start recording in background thread
    log("🚀 Starting recording service in background thread...")
    recording_thread = threading.Thread(target=recording_loop, daemon=True)
    recording_thread.start()
    
    # Start Flask web server on port 8000 (Azure Web Apps use PORT env var)
    port = int(os.environ.get('PORT', 8000))
    log(f"🌐 Starting Flask web server on port {port}...")
    app.run(host='0.0.0.0', port=port, debug=False)

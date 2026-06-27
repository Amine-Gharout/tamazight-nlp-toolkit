#!/usr/bin/env python3
"""
Radio Chaine 2 - Azure Blob Storage Recorder
Records live radio stream and uploads to Azure Blob Storage
Optimized for Azure VM deployment
"""

import subprocess
import tempfile
import os
import time
from datetime import datetime
from azure.storage.blob import BlobServiceClient

# ============= CONFIGURATION =============
import os

# Load from environment variables (set in .env or system env)
AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
if not AZURE_STORAGE_CONNECTION_STRING:
    raise ValueError(
        "AZURE_STORAGE_CONNECTION_STRING environment variable not set")

STREAM_URL = "https://radiochaine2.ice.infomaniak.ch/chaine2.mp3"
CONTAINER_NAME = "recordings"
CHUNK_DURATION = 300  # 5 minutes in seconds

# ============= INITIALIZATION =============
print("🔧 Initializing Azure Blob Storage connection...")
blob_service_client = BlobServiceClient.from_connection_string(
    AZURE_STORAGE_CONNECTION_STRING)
container_client = blob_service_client.get_container_client(CONTAINER_NAME)

# Create container if it doesn't exist
try:
    container_client.create_container()
    print(f"✅ Container '{CONTAINER_NAME}' created")
except Exception:
    print(f"✅ Container '{CONTAINER_NAME}' already exists")

# ============= FUNCTIONS =============


def record_chunk(chunk_number):
    """
    Record one chunk of the live stream to a temporary file
    Returns: tuple (success, temp_file_path, file_size_mb)
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    temp_file = os.path.join(tempfile.gettempdir(),
                             f"radio_temp_{timestamp}.mp3")

    print(f"\n🎙️  Recording chunk #{chunk_number}...")
    print(f"🕐 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    try:
        cmd = [
            "ffmpeg",
            "-i", STREAM_URL,
            "-t", str(CHUNK_DURATION),
            "-acodec", "libmp3lame",
            "-ab", "128k",
            "-y",
            temp_file
        ]

        print(f"📡 Connecting to stream...")
        result = subprocess.run(cmd, capture_output=True,
                                timeout=CHUNK_DURATION + 30)

        if os.path.exists(temp_file) and os.path.getsize(temp_file) > 10000:
            file_size = os.path.getsize(temp_file) / (1024 * 1024)
            print(f"✅ Recording completed ({file_size:.2f} MB)")
            return True, temp_file, file_size
        else:
            print(f"❌ Recording failed - file too small")
            if os.path.exists(temp_file):
                os.remove(temp_file)
            return False, None, 0

    except subprocess.TimeoutExpired:
        if os.path.exists(temp_file) and os.path.getsize(temp_file) > 10000:
            file_size = os.path.getsize(temp_file) / (1024 * 1024)
            print(f"⚠️  Timeout but file is valid ({file_size:.2f} MB)")
            return True, temp_file, file_size
        else:
            print(f"❌ Timeout and file incomplete")
            if os.path.exists(temp_file):
                os.remove(temp_file)
            return False, None, 0

    except Exception as e:
        print(f"❌ Recording error: {e}")
        if os.path.exists(temp_file):
            os.remove(temp_file)
        return False, None, 0


def upload_to_azure(temp_file, chunk_number, file_size):
    """
    Upload recorded file to Azure Blob Storage
    Returns: bool (success)
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    blob_name = f"radio_chaine2_{timestamp}_chunk{chunk_number}.mp3"

    try:
        print(f"☁️  Uploading to Azure...")

        blob_client = blob_service_client.get_blob_client(
            container=CONTAINER_NAME,
            blob=blob_name
        )

        with open(temp_file, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)

        print(f"✅ Uploaded successfully!")
        print(f"📦 Blob: {blob_name}")
        print(f"💾 Size: {file_size:.2f} MB")

        # Clean up temp file
        os.remove(temp_file)
        print(f"🗑️  Temp file removed")

        return True

    except Exception as e:
        print(f"❌ Upload error: {e}")
        if os.path.exists(temp_file):
            os.remove(temp_file)
        return False


# ============= MAIN LOOP =============
def main():
    """Main recording loop"""
    print("="*60)
    print("🔴 RADIO CHAINE 2 - CONTINUOUS RECORDER")
    print("="*60)
    print(f"📻 Stream: {STREAM_URL}")
    print(
        f"⏱️  Chunk Duration: {CHUNK_DURATION} seconds ({CHUNK_DURATION//60} minutes)")
    print(f"☁️  Azure Container: {CONTAINER_NAME}")
    print(f"🕐 Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)

    chunk_counter = 1
    success_count = 0
    fail_count = 0

    while True:
        try:
            print(f"\n{'='*60}")
            print(f"🎬 CHUNK #{chunk_counter}")
            print(f"{'='*60}")

            # Record chunk
            success, temp_file, file_size = record_chunk(chunk_counter)

            if success:
                # Upload to Azure
                upload_success = upload_to_azure(
                    temp_file, chunk_counter, file_size)

                if upload_success:
                    success_count += 1
                    print(
                        f"\n✅ Chunk #{chunk_counter} completed successfully!")
                else:
                    fail_count += 1
                    print(f"\n⚠️  Chunk #{chunk_counter} - upload failed")
            else:
                fail_count += 1
                print(f"\n⚠️  Chunk #{chunk_counter} - recording failed")

            # Statistics
            print(
                f"\n📊 Statistics: {success_count} successful, {fail_count} failed")

            chunk_counter += 1

            # Small delay before next chunk
            print(f"\n⏸️  Waiting 2 seconds before next chunk...")
            time.sleep(2)

        except KeyboardInterrupt:
            print("\n\n" + "="*60)
            print("⏹️  RECORDING STOPPED BY USER")
            print("="*60)
            print(f"📊 Total chunks: {chunk_counter - 1}")
            print(f"✅ Successful: {success_count}")
            print(f"❌ Failed: {fail_count}")
            print(f"☁️  Files saved in Azure Blob: {CONTAINER_NAME}")
            print(f"🕐 Stopped: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print("="*60)
            break

        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
            print(f"⏸️  Waiting 10 seconds before retry...")
            time.sleep(10)  # Wait before retry to avoid rapid failures


if __name__ == "__main__":
    main()

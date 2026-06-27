# 09 — Deployment

Azure cloud infrastructure for continuous Kabyle radio recording and storage.

## Contents

| File | Description |
|------|-------------|
| `AZURE_DEPLOYMENT.md` | Step-by-step Azure deployment guide (PowerShell) |
| `startup.sh` | VM startup script for auto-starting the recorder |
| `radio_recorder_vm_standalone.py` | Records Radio Chaine 2, uploads to Azure Blob Storage |
| `radio_recorder_azure_vm.py` | Optimized version for Azure VM deployment |
| `azure_webapp_recorder.py` | Azure Web App version of the recorder |
| `azure_webapp_recorder_old.py` | Archived earlier version |

## Pipeline

```
Radio Chaine 2 (MP3 stream)
        │
        ▼ ffmpeg (5-min chunks)
   Azure VM / ACI
        │
        ▼ Azure Blob Storage
   recordings/
```

Recordings are chunked into 5-minute MP3 segments and uploaded to Azure Blob Storage for later transcription and archiving.

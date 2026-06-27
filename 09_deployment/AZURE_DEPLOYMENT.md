# Azure Radio Recorder Deployment Guide

## Quick Start (Windows PowerShell)

### 1. Install Azure CLI
```powershell
winget install Microsoft.AzureCLI
```

### 2. Login to Azure
```powershell
az login
```

### 3. Set Variables
```powershell
$RESOURCE_GROUP = "radio-transcription-rg"
$LOCATION = "eastus"
$STORAGE_ACCOUNT = "radiotranscript" + (Get-Date -Format "yyyyMMddHHmmss")
$CONTAINER_REGISTRY = "radiotranscriptionacr"
$CONTAINER_NAME = "recordings"
$ACI_NAME = "radio-recorder"
```

### 4. Create Resource Group
```powershell
az group create --name $RESOURCE_GROUP --location $LOCATION
```

### 5. Create Storage Account
```powershell
az storage account create `
  --name $STORAGE_ACCOUNT `
  --resource-group $RESOURCE_GROUP `
  --location $LOCATION `
  --sku Standard_LRS
```

### 6. Get Connection String
```powershell
$CONNECTION_STRING = az storage account show-connection-string `
  --name $STORAGE_ACCOUNT `
  --resource-group $RESOURCE_GROUP `
  --query connectionString -o tsv
```

### 7. Create Blob Container
```powershell
az storage container create `
  --name $CONTAINER_NAME `
  --connection-string $CONNECTION_STRING
```

### 8. Create Azure Container Registry
```powershell
az acr create `
  --resource-group $RESOURCE_GROUP `
  --name $CONTAINER_REGISTRY `
  --sku Basic `
  --admin-enabled true
```

### 9. Build and Push Docker Image
```powershell
az acr build `
  --registry $CONTAINER_REGISTRY `
  --image radio-recorder:latest `
  --file Dockerfile `
  .
```

### 10. Deploy Container Instance
```powershell
az container create `
  --resource-group $RESOURCE_GROUP `
  --name $ACI_NAME `
  --image "$CONTAINER_REGISTRY.azurecr.io/radio-recorder:latest" `
  --cpu 1 `
  --memory 2 `
  --restart-policy Always `
  --registry-login-server "$CONTAINER_REGISTRY.azurecr.io" `
  --registry-username (az acr credential show --name $CONTAINER_REGISTRY --query username -o tsv) `
  --registry-password (az acr credential show --name $CONTAINER_REGISTRY --query "passwords[0].value" -o tsv) `
  --environment-variables `
    AZURE_STORAGE_CONNECTION_STRING="$CONNECTION_STRING" `
    CONTAINER_NAME="$CONTAINER_NAME"
```

## Monitoring

### View Logs
```powershell
az container logs --resource-group $RESOURCE_GROUP --name $ACI_NAME --follow
```

### Check Status
```powershell
az container show --resource-group $RESOURCE_GROUP --name $ACI_NAME --query instanceView.state
```

### List Recorded Files
```powershell
az storage blob list `
  --container-name $CONTAINER_NAME `
  --connection-string $CONNECTION_STRING `
  --output table
```

## Management

### Stop Container
```powershell
az container stop --resource-group $RESOURCE_GROUP --name $ACI_NAME
```

### Restart Container
```powershell
az container restart --resource-group $RESOURCE_GROUP --name $ACI_NAME
```

### Delete Container
```powershell
az container delete --resource-group $RESOURCE_GROUP --name $ACI_NAME --yes
```

### Delete All Resources
```powershell
az group delete --name $RESOURCE_GROUP --yes
```

## Cost Estimation

- **Azure Container Instance**: ~$30-40/month (1 vCPU, 2GB RAM, always running)
- **Azure Blob Storage**: ~$0.50-2/month (depending on data volume)
- **Container Registry**: ~$5/month (Basic tier)

**Total: ~$35-47/month**

## Alternative: Azure VM (Lower Cost)

1. Create Ubuntu VM (~$10-15/month)
2. Install dependencies:
   ```bash
   sudo apt update
   sudo apt install python3-pip ffmpeg
   pip3 install -r requirements_azure.txt
   ```

3. Create systemd service:
   ```bash
   sudo nano /etc/systemd/system/radio-recorder.service
   ```

4. Service file content:
   ```ini
   [Unit]
   Description=Radio Recorder Service
   After=network.target

   [Service]
   Type=simple
   User=azureuser
   WorkingDirectory=/home/azureuser/radio-recorder
   Environment="AZURE_STORAGE_CONNECTION_STRING=your_connection_string"
   ExecStart=/usr/bin/python3 /home/azureuser/radio-recorder/radio_recorder_azure.py
   Restart=always
   RestartSec=10

   [Install]
   WantedBy=multi-user.target
   ```

5. Enable and start:
   ```bash
   sudo systemctl enable radio-recorder
   sudo systemctl start radio-recorder
   sudo systemctl status radio-recorder
   ```

# Download recordings using Azure CLI (replace YOUR_ACCOUNT_KEY with your actual key)
# az storage blob list --container-name recordings --account-name radiotranscription --account-key "YOUR_ACCOUNT_KEY" --query "[].name" -o tsv | ForEach-Object { az storage blob download --container-name recordings --name $_ --file "downloaded_recordings/$_" --account-name radiotranscription --account-key "YOUR_ACCOUNT_KEY" }
 Enable shell integration to improve command detection


Get-ChildItem "downloaded_recordings" -Filter "*.mp3" | Measure-Object -Property Length -Sum | Select-Object @{Name="TotalFiles";Expression={$_.Count}}, @{Name="TotalSizeMB";Expression={[math]::Round($_.Sum/1MB, 2)}}
 Enable shell integration to improve command detection

Perfect! ✅ The script is now running with skip logic:

⏭️ Skips files that already exist locally
📥 Downloads only new files
📊 Shows progress for each file
Current status:

153 files already downloaded
687 MB total size
The download will continue and skip the 153 files you already have, only downloading the remaining ~369 recordings. This saves time and bandwidth!

The final summary will show:

How many were downloaded
How many were skipped
Total location of files
Claude Sonnet 4.5 • 1x
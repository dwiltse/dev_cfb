from azure.storage.blob import BlobServiceClient
import json
from typing import Any, Dict, List

class AzureStorageClient:
    def __init__(self, connection_string: str, container_name: str):
        self.blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        self.container_client = self.blob_service_client.get_container_client(container_name)
    
    def upload_json_data(self, data: List[Dict[str, Any]], blob_name: str) -> None:
        """Upload JSON data to Azure Blob Storage"""
        json_data = json.dumps(data)
        blob_client = self.container_client.get_blob_client(blob_name)
        blob_client.upload_blob(json_data, overwrite=True)
    
    def download_json_data(self, blob_name: str) -> List[Dict[str, Any]]:
        """Download and parse JSON data from Azure Blob Storage"""
        blob_client = self.container_client.get_blob_client(blob_name)
        data = blob_client.download_blob().readall()
        return json.loads(data)
import os
from api.cfbd_client import CFBDataClient
from storage.azure_storage import AzureStorageClient
from utils.secrets import SecretsManager

def main():
    # Initialize secrets manager
    vault_url = os.getenv('AZURE_KEY_VAULT_URL')
    if not vault_url:
        raise ValueError("Please set AZURE_KEY_VAULT_URL environment variable")
    
    secrets = SecretsManager(vault_url)
    
    # Get secrets from Key Vault
    cfbd_api_key = secrets.get_secret('cfbd-api-key')
    azure_connection_string = secrets.get_secret('azure-storage-connection-string')
    container_name = secrets.get_secret('azure-container-name')

    # Initialize clients
    cfbd_client = CFBDataClient(cfbd_api_key)
    azure_client = AzureStorageClient(azure_connection_string, container_name)

    # Fetch teams data
    teams_data = cfbd_client.get_teams()
    
    # Store in Azure Blob Storage
    azure_client.upload_json_data(teams_data, 'teams/teams.json')
    print(f"Successfully fetched and stored {len(teams_data)} teams")

if __name__ == '__main__':
    main()
import os
from dotenv import load_dotenv
load_dotenv()
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

    # Fetch FBS teams data for a specific year
    year = 2023
    teams_data = cfbd_client.get_fbs_teams(year=year)

    # Try to extract the year from the teams_data if available, else use the requested year
    actual_year = year
    if teams_data and isinstance(teams_data, list):
        first_team = teams_data[0]
        if isinstance(first_team, dict) and 'year' in first_team:
            actual_year = first_team['year']

    # Store in Azure Blob Storage
    blob_name = f"cfbd/teams/{actual_year}_teams.json"
    print(f"Uploading to container: {container_name}, blob: {blob_name}")
    azure_client.upload_json_data(teams_data, blob_name)
    print(f"Successfully fetched and stored {len(teams_data)} teams")


if __name__ == '__main__':
    main()
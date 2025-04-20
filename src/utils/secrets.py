from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

class SecretsManager:
    def __init__(self, vault_url: str):
        """Initialize the secrets manager with your Azure Key Vault URL"""
        self.credential = DefaultAzureCredential()
        self.client = SecretClient(vault_url=vault_url, credential=self.credential)

    def get_secret(self, secret_name: str) -> str:
        """Retrieve a secret from Azure Key Vault"""
        try:
            return self.client.get_secret(secret_name).value
        except Exception as e:
            raise Exception(f"Failed to retrieve secret {secret_name}: {str(e)}")
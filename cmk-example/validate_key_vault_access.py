from azure.identity import DefaultAzureCredential
from azure.keyvault.keys import KeyClient
from azure.keyvault.keys.crypto import CryptographyClient, EncryptionAlgorithm
from azure.core.exceptions import HttpResponseError
import os
from dotenv import load_dotenv

# === LOAD ENVIRONMENT VARIABLES ===
# Look for .env in the current directory
load_dotenv()

KEY_VAULT_URI = os.getenv("AZURE_KEY_VAULT_URI")
KEY_NAME = os.getenv("AZURE_KEY_VAULT_NAME")
KEY_VERSION = os.getenv("AZURE_KEY_VAULT_VERSION")  # Leave blank for latest version, or specify version string

print("KEY_VAULT_URI:", KEY_VAULT_URI)
print("KEY_NAME:", KEY_NAME)
print("KEY_VERSION:", KEY_VERSION)

# === AUTHENTICATION ===
credential = DefaultAzureCredential()

try:
    # Connect to Key Vault and retrieve the key
    key_client = KeyClient(vault_url=KEY_VAULT_URI, credential=credential)
    if KEY_VERSION:
        key = key_client.get_key(KEY_NAME, KEY_VERSION)
        print(f"Key '{KEY_NAME}' (version: {KEY_VERSION}) retrieved successfully.")
    else:
        key = key_client.get_key(KEY_NAME)
        print(f"Key '{KEY_NAME}' (latest version) retrieved successfully.")

    # Create a CryptographyClient for cryptographic operations
    crypto_client = CryptographyClient(key, credential=credential)

    # Test wrap/unwrap operation (requires correct permissions)
    plaintext = b"0123456789abcdef0123456789abcdef"  # 32 bytes
    wrap_result = crypto_client.wrap_key(EncryptionAlgorithm.rsa_oaep, plaintext)
    print("Wrap operation succeeded.")

    unwrap_result = crypto_client.unwrap_key(EncryptionAlgorithm.rsa_oaep, wrap_result.encrypted_key)
    print("Unwrap operation succeeded.")

    if unwrap_result.key == plaintext:
        print("Validation successful: Access and cryptographic permissions are correct!")
    else:
        print("Validation failed: Unwrapped key does not match original.")

except HttpResponseError as e:
    print(f"HTTP error: {e.message}")
except Exception as ex:
    print(f"Error: {ex}") 
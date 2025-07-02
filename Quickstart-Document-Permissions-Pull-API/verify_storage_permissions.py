from azure.storage.filedatalake import DataLakeServiceClient
from azure.identity import DefaultAzureCredential
import os
from dotenv import load_dotenv
import base64
import json

load_dotenv(override=True)

# Print environment variables for debugging
adls_gen2_connection_string = os.environ["AZURE_STORAGE_CONNECTION_STRING"]
adls_gen2_container_name = os.getenv("AZURE_STORAGE_CONTAINER_NAME")
print(adls_gen2_connection_string)
print(adls_gen2_container_name)
print("PATH:", os.environ["PATH"])

# Print the Azure identity being used (if available)
try:
    import subprocess
    result = subprocess.run(["az", "account", "show", "--query", "user"], capture_output=True, text=True)
    if result.returncode == 0:
        print("Azure CLI authenticated user:", result.stdout.strip())
    else:
        print("Could not determine Azure CLI user. Not authenticated via Azure CLI or az not installed.")
except Exception as e:
    print(f"Error checking Azure CLI user: {e}")

# Try calling az.cmd directly from the known path
print("\n--- Attempting to get Azure CLI user via az.cmd ---")
az_cmd_path = r"C:\Program Files\Microsoft SDKs\Azure\CLI2\wbin\az.cmd"
try:
    result = subprocess.run([az_cmd_path, "account", "show", "--query", "user"], capture_output=True, text=True)
    if result.returncode == 0:
        print("Azure CLI authenticated user (via az.cmd):", result.stdout.strip())
    else:
        print("Could not determine Azure CLI user via az.cmd. Return code:", result.returncode)
        print("stderr:", result.stderr)
except Exception as e:
    print(f"Error checking Azure CLI user via az.cmd: {e}")

# Decode the Azure access token to print identity info
print("\n--- Decoding Azure access token to show identity info ---")
try:
    token = DefaultAzureCredential().get_token("https://storage.azure.com/.default").token
    # JWT tokens are in the format header.payload.signature
    payload = token.split(".")[1]
    # Pad base64 if needed
    padding = '=' * (-len(payload) % 4)
    decoded = base64.urlsafe_b64decode(payload + padding)
    claims = json.loads(decoded)
    print("Token claims:")
    for k in ["oid", "upn", "email", "name", "appid", "tid"]:
        if k in claims:
            print(f"  {k}: {claims[k]}")
except Exception as e:
    print(f"Error decoding access token: {e}")

credential = DefaultAzureCredential()
service = DataLakeServiceClient.from_connection_string(adls_gen2_connection_string, credential=credential)
container = service.get_file_system_client(adls_gen2_container_name)

# Create the container if it doesn't exist
if not container.exists():
    print("Container does not exist. Creating container...")
    container.create_file_system()
else:
    print("Container exists.")

# Try to create a test directory
test_dir_name = "test-directory"
test_dir_client = container.get_directory_client(test_dir_name)
try:
    test_dir_client.create_directory()
    print(f"Directory '{test_dir_name}' created successfully.")
except Exception as e:
    print(f"Failed to create directory: {e}") 
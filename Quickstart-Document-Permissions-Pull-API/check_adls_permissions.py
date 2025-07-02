from azure.storage.filedatalake import DataLakeServiceClient
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from dotenv import load_dotenv
import os
import requests
import sys

print("--- Step 1: Load environment variables ---")
load_dotenv(override=True)
try:
    endpoint = os.environ["AZURE_SEARCH_ENDPOINT"]
    adls_gen2_connection_string = os.environ["AZURE_STORAGE_CONNECTION_STRING"]
    adls_gen2_account_name = os.getenv("AZURE_STORAGE_ACCOUNT_NAME")
    adls_gen2_container_name = os.getenv("AZURE_STORAGE_CONTAINER_NAME")
    adls_gen2_resource_id = os.environ["AZURE_STORAGE_RESOURCE_ID"]
    print("Environment variables loaded successfully.")
    print(f"  endpoint: {endpoint}")
    print(f"  adls_gen2_account_name: {adls_gen2_account_name}")
    print(f"  adls_gen2_container_name: {adls_gen2_container_name}")
except Exception as e:
    print(f"Failed to load environment variables: {e}")
    sys.exit(1)

print("\n--- Step 2: Authenticate with Azure ---")
try:
    credential = DefaultAzureCredential()
    token_provider = get_bearer_token_provider(credential, "https://search.azure.com/.default")
    print("Azure authentication successful.")
except Exception as e:
    print(f"Azure authentication failed: {e}")
    sys.exit(1)

print("\n--- Step 3: Retrieve group IDs from Microsoft Graph ---")
try:
    token = credential.get_token("https://graph.microsoft.com/.default").token
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get("https://graph.microsoft.com/v1.0/me/memberOf?$select=id,displayName", headers=headers)
    groups = response.json()["value"]
    first_group_id = groups[0]["id"]
    second_group_id = groups[1]["id"]
    print(f"First group ID: {first_group_id}")
    print(f"Second group ID: {second_group_id}")
except Exception as e:
    print(f"Failed to retrieve group IDs: {e}")
    sys.exit(1)

print("\n--- Step 4: Connect to ADLS Gen2 and create container if needed ---")
try:
    service = DataLakeServiceClient.from_connection_string(adls_gen2_connection_string, credential=credential)
    container = service.get_file_system_client(adls_gen2_container_name)
    if not container.exists():
        container.create_file_system()
        print("Container created.")
    else:
        print("Container exists.")
except Exception as e:
    print(f"Failed to connect to or create container: {e}")
    sys.exit(1)

print("\n--- Step 5: Create 'state-parks' directory ---")
try:
    state_parks_dir_client = container.get_directory_client("state-parks")
    state_parks_dir_client.create_directory()
    print("'state-parks' directory created.")
except Exception as e:
    print(f"Failed to create 'state-parks' directory: {e}")

print("\n--- Step 6: Set ACLs on root directory ---")
try:
    root_dir_client = container.get_directory_client("/")
    root_dir_client.update_access_control_recursive(f"group:{first_group_id}:rwx")
    print(f"Root ACL set for first group: {first_group_id}")
    root_dir_client.update_access_control_recursive(f"group:{second_group_id}:rwx")
    print(f"Root ACL set for second group: {second_group_id}")
except Exception as e:
    print(f"Failed to set root ACLs: {e}")

print("\n--- Step 7: Create and upload to 'oregon' subdirectory ---")
try:
    oregon_dir_client = state_parks_dir_client.create_sub_directory("oregon")
    oregon_dir_client.create_directory()
    file_client = oregon_dir_client.create_file("oregon_state_parks.csv")
    oregon_state_parks_content = requests.get("https://raw.githubusercontent.com/Azure-Samples/azure-search-sample-data/refs/heads/main/state-parks/Oregon/oregon_state_parks.csv").content.decode("utf-8")
    file_client.upload_data(oregon_state_parks_content, overwrite=True)
    oregon_dir_client.update_access_control_recursive(f"group:{first_group_id}:rwx")
    print("'oregon' subdirectory and file created, ACL set.")
except Exception as e:
    print(f"Failed with 'oregon' subdirectory or file: {e}")

print("\n--- Step 8: Create and upload to 'washington' subdirectory ---")
try:
    washington_dir_client = state_parks_dir_client.create_sub_directory("washington")
    washington_dir_client.create_directory()
    file_client = washington_dir_client.create_file("washington_state_parks.csv")
    washington_state_parks_content = requests.get("https://raw.githubusercontent.com/Azure-Samples/azure-search-sample-data/refs/heads/main/state-parks/Washington/washington_state_parks.csv").content.decode("utf-8")
    file_client.upload_data(washington_state_parks_content, overwrite=True)
    washington_dir_client.update_access_control_recursive(f"group:{second_group_id}:rwx")
    print("'washington' subdirectory and file created, ACL set.")
except Exception as e:
    print(f"Failed with 'washington' subdirectory or file: {e}") 
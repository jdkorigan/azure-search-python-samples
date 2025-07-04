from azure.identity import DefaultAzureCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.core.exceptions import HttpResponseError
import os
from dotenv import load_dotenv
import sys

# === LOAD ENVIRONMENT VARIABLES ===
load_dotenv()

SEARCH_SERVICE_ENDPOINT = os.getenv("AZURE_SEARCH_SERVICE")
SEARCH_INDEX_NAME = os.getenv("AZURE_SEARCH_INDEX_NAME")

print("SEARCH_SERVICE_ENDPOINT:", SEARCH_SERVICE_ENDPOINT)
print("SEARCH_INDEX_NAME:", SEARCH_INDEX_NAME)

if not SEARCH_SERVICE_ENDPOINT:
    print("ERROR: AZURE_SEARCH_SERVICE_ENDPOINT is not set in the .env file.")
    sys.exit(1)

# === AUTHENTICATION ===
credential = DefaultAzureCredential()

try:
    # Connect to Search Service
    index_client = SearchIndexClient(endpoint=SEARCH_SERVICE_ENDPOINT, credential=credential)
    print("Connected to Azure AI Search service.")

    # List indexes
    indexes = list(index_client.list_indexes())
    print(f"Found {len(indexes)} indexes:")
    for idx in indexes:
        print(" -", idx.name)

    # Try to get the specified index
    if SEARCH_INDEX_NAME:
        index = index_client.get_index(SEARCH_INDEX_NAME)
        print(f"Index '{SEARCH_INDEX_NAME}' retrieved successfully.")
    else:
        print("No index name specified in .env (AZURE_SEARCH_INDEX_NAME). Skipping index retrieval.")

    print("Validation successful: Access to Azure AI Search service is working!")

except HttpResponseError as e:
    print(f"HTTP error: {e.message}")
except Exception as ex:
    print(f"Error: {ex}") 
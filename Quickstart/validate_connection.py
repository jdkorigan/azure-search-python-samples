#!/usr/bin/env python3
"""
Connection validation script for Azure AI Search
This script tests the connection to your Azure Search service.
"""

import os
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.core.exceptions import ServiceRequestError, HttpResponseError

def validate_connection():
    """Validate the connection to Azure Search service."""
    print("🔍 Validating Azure Search connection...")
    
    # Load environment variables
    load_dotenv()
    
    search_endpoint = os.getenv('SEARCH-ENDPOINT')
    search_api_key = os.getenv('SEARCH-API-KEY')
    
    if not search_endpoint or not search_api_key:
        print("❌ Missing environment variables!")
        print("Please ensure SEARCH-ENDPOINT and SEARCH-API-KEY are set in your .env file")
        return False
    
    print(f"📍 Endpoint: {search_endpoint}")
    print(f"🔑 API Key: {'*' * (len(search_api_key) - 4) + search_api_key[-4:]}")
    
    try:
        # Create credential and client
        credential = AzureKeyCredential(search_api_key)
        index_client = SearchIndexClient(endpoint=search_endpoint, credential=credential)
        
        # Test connection by listing indexes
        print("\n🔄 Testing connection...")
        indexes = list(index_client.list_indexes())
        
        print(f"✅ Connection successful!")
        print(f"📊 Found {len(indexes)} existing indexes:")
        for index in indexes:
            print(f"   - {index.name}")
        
        return True
        
    except ServiceRequestError as e:
        print(f"❌ Connection failed: {e}")
        print("\nPossible causes:")
        print("- Invalid endpoint URL")
        print("- Network connectivity issues")
        print("- DNS resolution problems")
        return False
        
    except HttpResponseError as e:
        print(f"❌ Authentication failed: {e}")
        print("\nPossible causes:")
        print("- Invalid API key")
        print("- Insufficient permissions")
        print("- Service not found")
        return False
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def main():
    print("🚀 Azure AI Search Connection Validator")
    print("=" * 40)
    
    if validate_connection():
        print("\n🎉 Your Azure Search service is ready to use!")
        print("You can now run the quickstart notebook.")
    else:
        print("\n❌ Connection validation failed.")
        print("Please check your configuration and try again.")

if __name__ == "__main__":
    main() 
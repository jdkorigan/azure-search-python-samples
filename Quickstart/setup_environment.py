#!/usr/bin/env python3
"""
Setup script for Azure AI Search Quickstart
This script helps you configure your environment variables for the Azure Search quickstart.
"""

import os
from pathlib import Path

def check_env_file():
    """Check if .env file exists and has the required variables."""
    env_file = Path('.env')
    
    if not env_file.exists():
        print("❌ No .env file found!")
        print("\nTo fix this issue:")
        print("1. Copy sample.env to .env:")
        print("   cp sample.env .env")
        print("2. Edit .env with your actual Azure Search service details")
        print("3. Run this script again to validate")
        return False
    
    # Load and check environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    search_endpoint = os.getenv('SEARCH-ENDPOINT')
    search_api_key = os.getenv('SEARCH-API-KEY')
    
    print("🔍 Checking environment variables...")
    
    if not search_endpoint:
        print("❌ SEARCH-ENDPOINT is not set")
        return False
    elif search_endpoint == "https://your-service-name.search.windows.net":
        print("❌ SEARCH-ENDPOINT still has the placeholder value")
        return False
    else:
        print(f"✅ SEARCH-ENDPOINT: {search_endpoint}")
    
    if not search_api_key:
        print("❌ SEARCH-API-KEY is not set")
        return False
    elif search_api_key == "your-admin-api-key-here":
        print("❌ SEARCH-API-KEY still has the placeholder value")
        return False
    else:
        print(f"✅ SEARCH-API-KEY: {'*' * (len(search_api_key) - 4) + search_api_key[-4:]}")
    
    return True

def create_env_file():
    """Create .env file from sample.env if it doesn't exist."""
    sample_env = Path('sample.env')
    env_file = Path('.env')
    
    if not sample_env.exists():
        print("❌ sample.env file not found!")
        return False
    
    if env_file.exists():
        print("⚠️  .env file already exists. Skipping creation.")
        return True
    
    try:
        import shutil
        shutil.copy(sample_env, env_file)
        print("✅ Created .env file from sample.env")
        print("📝 Please edit .env with your actual Azure Search service details")
        return True
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        return False

def main():
    print("🚀 Azure AI Search Quickstart Environment Setup")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path('azure-search-quickstart.ipynb').exists():
        print("❌ Please run this script from the Quickstart directory")
        return
    
    # Try to create .env file if it doesn't exist
    if not Path('.env').exists():
        print("📁 Creating .env file...")
        if not create_env_file():
            return
    
    # Check environment variables
    if check_env_file():
        print("\n🎉 Environment is properly configured!")
        print("You can now run the Azure Search quickstart notebook.")
    else:
        print("\n❌ Environment is not properly configured.")
        print("Please fix the issues above and run this script again.")

if __name__ == "__main__":
    main() 
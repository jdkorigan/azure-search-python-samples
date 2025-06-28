#!/usr/bin/env python3
"""
Script to check the exact region of your Azure OpenAI service using Azure CLI or REST API.
"""

import os
import subprocess
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)

def check_with_azure_cli():
    """Check region using Azure CLI"""
    print("🔍 CHECKING REGION WITH AZURE CLI")
    print("=" * 50)
    
    try:
        # Get the service name from endpoint
        azure_openai_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
        if not azure_openai_endpoint:
            print("❌ AZURE_OPENAI_ENDPOINT not found")
            return None
            
        service_name = azure_openai_endpoint.replace("https://", "").split(".")[0]
        print(f"Service Name: {service_name}")
        
        # Run Azure CLI command to get resource details
        cmd = f"az cognitiveservices account show --name {service_name} --resource-group * --query 'location' --output tsv"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            region = result.stdout.strip()
            print(f"✅ Region: {region}")
            return region
        else:
            print(f"❌ Azure CLI error: {result.stderr}")
            return None
            
    except Exception as e:
        print(f"❌ Error running Azure CLI: {e}")
        return None

def check_supported_regions():
    """Check if a region supports Responses API"""
    print("\n📋 CHECKING RESPONSES API SUPPORT")
    print("=" * 50)
    
    supported_regions = [
        "East US",
        "West US 2", 
        "North Europe",
        "West Europe",
        "UK South",
        "Australia East",
        "Canada East"
    ]
    
    # Common region mappings
    region_mappings = {
        "eastus": "East US",
        "westus2": "West US 2",
        "northeurope": "North Europe", 
        "westeurope": "West Europe",
        "uksouth": "UK South",
        "australiaeast": "Australia East",
        "canadaeast": "Canada East"
    }
    
    return supported_regions, region_mappings

def check_region_support(region):
    """Check if the given region supports Responses API"""
    supported_regions, region_mappings = check_supported_regions()
    
    print(f"Checking region: {region}")
    
    # Check exact match
    if region in supported_regions:
        print("✅ This region supports the Responses API!")
        return True
    
    # Check mapped region
    region_lower = region.lower()
    for pattern, mapped_region in region_mappings.items():
        if pattern in region_lower or region_lower in pattern:
            if mapped_region in supported_regions:
                print(f"✅ This region ({mapped_region}) supports the Responses API!")
                return True
    
    print("❌ This region does NOT support the Responses API.")
    return False

def show_european_options():
    """Show European region options"""
    print("\n🌍 EUROPEAN REGION OPTIONS")
    print("=" * 50)
    
    european_regions = [
        "North Europe",
        "West Europe", 
        "UK South"
    ]
    
    print("European regions that support Responses API:")
    for region in european_regions:
        print(f"  • {region}")
    
    print("\nIf you're in a different European region, you can:")
    print("1. Create a new Azure OpenAI service in North Europe or West Europe")
    print("2. Contact Azure support to request Responses API in your region")
    print("3. Use Chat Completions API as an alternative")

def main():
    print("🚀 AZURE OPENAI REGION DETECTOR")
    print("=" * 60)
    
    # Try to get region with Azure CLI
    region = check_with_azure_cli()
    
    if region:
        # Check if it supports Responses API
        supports_responses = check_region_support(region)
        
        if not supports_responses:
            show_european_options()
    else:
        print("\n⚠️  Could not determine region automatically.")
        print("Please check manually in Azure Portal:")
        print("1. Go to https://portal.azure.com")
        print("2. Find your Azure OpenAI service (kor-ai-hub-3)")
        print("3. Check the 'Location' field in the Overview")
        print("4. Compare with supported regions below:")
        
        supported_regions, _ = check_supported_regions()
        print("\nSupported regions for Responses API:")
        for region in supported_regions:
            print(f"  • {region}")
    
    print("\n" + "=" * 60)
    print("NEXT STEPS:")
    print("=" * 60)
    print("If your region doesn't support Responses API:")
    print("1. Create new service in North Europe or West Europe")
    print("2. Deploy your model in the new service")
    print("3. Update your .env file")
    print("4. Test with: python check_responses_api.py")

if __name__ == "__main__":
    main() 
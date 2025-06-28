#!/usr/bin/env python3
"""
Script to check the region of your Azure OpenAI service.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)

def check_service_region():
    """Check the region of the Azure OpenAI service"""
    print("🌍 CHECKING AZURE OPENAI SERVICE REGION")
    print("=" * 50)
    
    azure_openai_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
    
    if not azure_openai_endpoint:
        print("❌ AZURE_OPENAI_ENDPOINT not found in .env file")
        return
    
    print(f"Endpoint: {azure_openai_endpoint}")
    
    # Try to extract region from endpoint
    if "openai.azure.com" in azure_openai_endpoint:
        # The region is typically in the service name
        service_name = azure_openai_endpoint.replace("https://", "").split(".")[0]
        print(f"Service Name: {service_name}")
        
        # Common region patterns in service names
        region_patterns = {
            "eastus": "East US",
            "westus2": "West US 2", 
            "northeurope": "North Europe",
            "westeurope": "West Europe",
            "uksouth": "UK South",
            "australiaeast": "Australia East",
            "canadaeast": "Canada East",
            "centralus": "Central US",
            "southcentralus": "South Central US",
            "westus": "West US",
            "eastus2": "East US 2",
            "brazilsouth": "Brazil South",
            "japaneast": "Japan East",
            "southeastasia": "Southeast Asia",
            "koreacentral": "Korea Central"
        }
        
        service_lower = service_name.lower()
        found_region = None
        
        for pattern, region_name in region_patterns.items():
            if pattern in service_lower:
                found_region = region_name
                break
        
        if found_region:
            print(f"Detected Region: {found_region}")
            
            # Check if it's a supported region for Responses API
            supported_regions = [
                "East US", "West US 2", "North Europe", "West Europe",
                "UK South", "Australia East", "Canada East"
            ]
            
            if found_region in supported_regions:
                print("✅ This region supports the Responses API!")
                print("The issue might be with your service configuration.")
            else:
                print("❌ This region does NOT support the Responses API.")
                print("You need to create a new service in a supported region.")
        else:
            print("⚠️  Could not determine region from service name.")
            print("Check your Azure portal for the exact region.")
    else:
        print("⚠️  Endpoint doesn't match expected Azure OpenAI format.")

def show_supported_regions():
    """Show supported regions for Responses API"""
    print("\n📋 RESPONSES API SUPPORTED REGIONS")
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
    
    print("The Responses API is available in these regions:")
    for region in supported_regions:
        print(f"  • {region}")
    
    print("\nTo use client.responses.create(), you need:")
    print("1. Azure OpenAI service in one of the above regions")
    print("2. API version 2025-05-01-Preview or later")
    print("3. Supported model deployment (gpt-4o, gpt-4o-mini, etc.)")

def main():
    print("🚀 AZURE OPENAI REGION CHECKER")
    print("=" * 60)
    
    check_service_region()
    show_supported_regions()
    
    print("\n" + "=" * 60)
    print("NEXT STEPS:")
    print("=" * 60)
    print("If your region doesn't support Responses API:")
    print("1. Create a new Azure OpenAI service in a supported region")
    print("2. Deploy your model in the new service")
    print("3. Update your .env file with the new endpoint")
    print("4. Test with: python check_responses_api.py")

if __name__ == "__main__":
    main() 
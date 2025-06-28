#!/usr/bin/env python3
"""
Diagnostic script to check if the Responses API is available in your Azure OpenAI service.
"""

from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
import os
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv(override=True)

def check_azure_openai_service():
    """Check Azure OpenAI service configuration"""
    print("🔍 DIAGNOSING AZURE OPENAI SERVICE")
    print("=" * 50)
    
    # Get configuration
    azure_openai_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
    azure_openai_api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2025-05-01-Preview")
    
    if not azure_openai_endpoint:
        print("❌ AZURE_OPENAI_ENDPOINT not found in .env file")
        return False
    
    print(f"✅ Endpoint: {azure_openai_endpoint}")
    print(f"✅ API Version: {azure_openai_api_version}")
    
    # Extract region from endpoint
    if "openai.azure.com" in azure_openai_endpoint:
        # Extract region from URL like: https://your-service.openai.azure.com
        parts = azure_openai_endpoint.replace("https://", "").split(".")
        if len(parts) >= 2:
            service_name = parts[0]
            print(f"✅ Service Name: {service_name}")
        else:
            print("⚠️  Could not extract service name from endpoint")
    else:
        print("⚠️  Endpoint doesn't match expected Azure OpenAI format")
    
    return True

def test_responses_api_availability():
    """Test if Responses API is available"""
    print("\n🧪 TESTING RESPONSES API AVAILABILITY")
    print("=" * 50)
    
    try:
        # Setup client
        azure_openai_endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
        azure_openai_api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2025-05-01-Preview")
        answer_model = os.getenv("ANSWER_MODEL", "gpt-4o")
        
        credential = DefaultAzureCredential()
        azure_openai_token_provider = get_bearer_token_provider(credential, "https://cognitiveservices.azure.com/.default")
        
        client = AzureOpenAI(
            azure_endpoint=azure_openai_endpoint,
            azure_ad_token_provider=azure_openai_token_provider,
            api_version=azure_openai_api_version
        )
        
        # Test with minimal request
        test_messages = [
            {"role": "user", "content": "Hello"}
        ]
        
        print(f"Testing with model: {answer_model}")
        print(f"Testing with API version: {azure_openai_api_version}")
        
        response = client.responses.create(
            model=answer_model,
            input=test_messages
        )
        
        print("✅ SUCCESS! Responses API is available!")
        print(f"Response: {response.output_text}")
        return True
        
    except Exception as e:
        print(f"❌ Responses API failed: {e}")
        
        # Provide specific guidance based on error
        if "404" in str(e):
            print("\n🔧 TROUBLESHOOTING 404 ERROR:")
            print("1. Check if your Azure OpenAI service is in a supported region:")
            print("   - East US, West US 2, North Europe, West Europe")
            print("   - UK South, Australia East, Canada East")
            print("2. Verify you're using the latest API version: 2025-05-01-Preview")
            print("3. Make sure your model deployment supports the Responses API")
            print("4. Check if your Azure OpenAI service was created recently")
        elif "401" in str(e):
            print("\n🔧 TROUBLESHOOTING 401 ERROR:")
            print("1. Check your authentication credentials")
            print("2. Verify you have the correct permissions")
        elif "400" in str(e):
            print("\n🔧 TROUBLESHOOTING 400 ERROR:")
            print("1. Check your model deployment name")
            print("2. Verify the model supports the Responses API")
        
        return False

def check_alternative_solutions():
    """Check alternative solutions"""
    print("\n💡 ALTERNATIVE SOLUTIONS")
    print("=" * 50)
    
    print("If Responses API is not available, you can:")
    print("1. Use Chat Completions API (works everywhere)")
    print("2. Contact Azure support to enable Responses API")
    print("3. Create a new Azure OpenAI service in a supported region")
    print("4. Wait for Responses API to be available in your region")

def main():
    print("🚀 AZURE OPENAI RESPONSES API DIAGNOSTIC")
    print("=" * 60)
    
    # Check service configuration
    if not check_azure_openai_service():
        return
    
    # Test Responses API
    success = test_responses_api_availability()
    
    if not success:
        check_alternative_solutions()
    
    print("\n" + "=" * 60)
    print("SUMMARY:")
    print("=" * 60)
    
    if success:
        print("✅ Your Azure OpenAI service supports the Responses API!")
        print("You can use client.responses.create() in your notebook.")
    else:
        print("❌ Responses API is not available in your current setup.")
        print("Consider using Chat Completions API as an alternative.")

if __name__ == "__main__":
    main() 
#!/usr/bin/env python3
"""
Fix for the Responses API 404 error in the Azure AI Search Agentic Retrieval notebook.

The responses API is not available in all Azure OpenAI regions. This script shows
how to use the standard Chat Completions API instead.
"""

from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)

# Configuration
azure_openai_endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
azure_openai_api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2025-03-01-preview")
answer_model = os.getenv("ANSWER_MODEL", "gpt-4o")

# Setup credentials
credential = DefaultAzureCredential()
azure_openai_token_provider = get_bearer_token_provider(credential, "https://cognitiveservices.azure.com/.default")

# Create Azure OpenAI client
client = AzureOpenAI(
    azure_endpoint=azure_openai_endpoint,
    azure_ad_token_provider=azure_openai_token_provider,
    api_version=azure_openai_api_version
)

# Sample messages (from your notebook)
messages = [
    {
        "role": "system",
        "content": "A Q&A agent that can answer questions about the Earth at night. Sources have a JSON format with a ref_id that must be cited in the answer. If you do not have the answer, respond with \"I don't know\"."
    },
    {
        "role": "user", 
        "content": "Why do suburban belts display larger December brightening than urban cores even though absolute light levels are higher downtown?"
    },
    {
        "role": "assistant",
        "content": "Based on the available information, I don't have specific data about December brightening patterns in suburban belts versus urban cores. The sources available don't contain detailed information about seasonal lighting variations or the specific comparison you're asking about."
    }
]

def try_responses_api():
    """Try to use the Responses API (may fail in some regions)"""
    try:
        print("Attempting to use Responses API...")
        response = client.responses.create(
            model=answer_model,
            input=messages
        )
        print("✅ Responses API worked!")
        print(f"Response: {response.output_text}")
        return True
    except Exception as e:
        print(f"❌ Responses API failed: {e}")
        return False

def use_chat_completions_api():
    """Use the standard Chat Completions API (works everywhere)"""
    try:
        print("Using Chat Completions API...")
        response = client.chat.completions.create(
            model=answer_model,
            messages=messages
        )
        print("✅ Chat Completions API worked!")
        print(f"Response: {response.choices[0].message.content}")
        return True
    except Exception as e:
        print(f"❌ Chat Completions API failed: {e}")
        return False

def main():
    print("Testing Azure OpenAI API endpoints...")
    print(f"Endpoint: {azure_openai_endpoint}")
    print(f"API Version: {azure_openai_api_version}")
    print(f"Model: {answer_model}")
    print("-" * 50)
    
    # Try Responses API first
    if not try_responses_api():
        print("\nFalling back to Chat Completions API...")
        use_chat_completions_api()
    
    print("\n" + "=" * 50)
    print("RECOMMENDATION:")
    print("Use the Chat Completions API for maximum compatibility.")
    print("Replace client.responses.create() with client.chat.completions.create()")
    print("Replace response.output_text with response.choices[0].message.content")

if __name__ == "__main__":
    main() 
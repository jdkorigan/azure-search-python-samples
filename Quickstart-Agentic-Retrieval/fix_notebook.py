#!/usr/bin/env python3
"""
Quick fix for the Responses API 404 error in the notebook.

Replace the problematic code in your notebook with this working version.
"""

# PROBLEMATIC CODE (causes 404 error):
"""
response = client.responses.create(
    model=answer_model,
    input=messages
)
wrapped = textwrap.fill(response.output_text, width=100)
"""

# WORKING CODE (replacement):
"""
response = client.chat.completions.create(
    model=answer_model,
    messages=messages
)
wrapped = textwrap.fill(response.choices[0].message.content, width=100)
"""

# Complete working example:
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
import os
from dotenv import load_dotenv
import textwrap

# Load environment variables
load_dotenv(override=True)

# Configuration
azure_openai_endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
azure_openai_api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2025-05-01-Preview")
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
    }
]

def test_responses_api():
    """Test if Responses API works (will likely fail)"""
    try:
        print("Testing Responses API...")
        response = client.responses.create(
            model=answer_model,
            input=messages
        )
        print("✅ Responses API works!")
        return response.output_text
    except Exception as e:
        print(f"❌ Responses API failed: {e}")
        return None

def test_chat_completions_api():
    """Test Chat Completions API (should work)"""
    try:
        print("Testing Chat Completions API...")
        response = client.chat.completions.create(
            model=answer_model,
            messages=messages
        )
        print("✅ Chat Completions API works!")
        return response.choices[0].message.content
    except Exception as e:
        print(f"❌ Chat Completions API failed: {e}")
        return None

def main():
    print("=" * 60)
    print("FIXING THE RESPONSES API 404 ERROR")
    print("=" * 60)
    
    print(f"Endpoint: {azure_openai_endpoint}")
    print(f"API Version: {azure_openai_api_version}")
    print(f"Model: {answer_model}")
    print()
    
    # Test both APIs
    responses_result = test_responses_api()
    print()
    chat_result = test_chat_completions_api()
    
    print("\n" + "=" * 60)
    print("SOLUTION:")
    print("=" * 60)
    
    if chat_result:
        print("✅ Use Chat Completions API - it works!")
        print("\nReplace this code in your notebook:")
        print("❌ PROBLEMATIC CODE:")
        print("response = client.responses.create(")
        print("    model=answer_model,")
        print("    input=messages")
        print(")")
        print("wrapped = textwrap.fill(response.output_text, width=100)")
        
        print("\n✅ WITH THIS WORKING CODE:")
        print("response = client.chat.completions.create(")
        print("    model=answer_model,")
        print("    messages=messages")
        print(")")
        print("wrapped = textwrap.fill(response.choices[0].message.content, width=100)")
        
        print(f"\nSample response: {chat_result[:100]}...")
    else:
        print("❌ Both APIs failed. Check your configuration.")

if __name__ == "__main__":
    main() 
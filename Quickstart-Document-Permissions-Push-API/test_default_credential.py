import os
from azure.identity import DefaultAzureCredential
from azure.core.exceptions import ClientAuthenticationError

# Try to get a token for Microsoft Graph
SCOPES = ["https://graph.microsoft.com/.default"]

try:
    credential = DefaultAzureCredential()
    token = credential.get_token(*SCOPES)
    print("Successfully obtained token!")
    print(f"Token: {token.token[:40]}... (truncated)")
except Exception as e:
    print("Failed to obtain token with DefaultAzureCredential.")
    print("Error:", e) 
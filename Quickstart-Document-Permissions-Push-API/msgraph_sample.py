import os
import asyncio
from azure.identity import DefaultAzureCredential
from msgraph import GraphServiceClient
from dotenv import load_dotenv  # For loading .env variables

# Load environment variables from .env file
load_dotenv()

# Read credentials from environment variables
SCOPES = ["https://graph.microsoft.com/.default"]

# Use DefaultAzureCredential for authentication
# This will use environment variables, managed identity, or developer credentials
credential = DefaultAzureCredential()
client = GraphServiceClient(credentials=credential, scopes=SCOPES)

async def main():
    # Get current user profile
    me = await client.me.get()
    print("User profile:")
    print(f"Display Name: {me.display_name}")
    print(f"User Principal Name: {me.user_principal_name}")
    print(f"ID: {me.id}")

    # Get group memberships
    print("\nGroup memberships:")
    groups = await client.me.member_of.get()
    if hasattr(groups, "value"):
        for group in groups.value:
            print(f"Group ID: {group.id}, Display Name: {getattr(group, 'display_name', 'N/A')}")
    else:
        print("No group memberships found.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print("An error occurred:", e) 
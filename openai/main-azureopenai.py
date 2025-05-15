import os
import sys
import httpx
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()

# endpoint should be in format:
# https://apim.contoso.com/openai/deployments/{deployment-id}/chat/completions?api-version=2024-02-15-preview
# E.g.,
# https://apim.contoso.com/openai/deployments/aoai/chat/completions?api-version=2024-02-15-preview
endpoint = os.getenv("ENDPOINT")
api_key = os.getenv("API_KEY")

if not api_key or not endpoint:
    print("Error: Azure OpenAI configuration is incomplete")
    print("Please set API_KEY and ENDPOINT in the .env file")
    sys.exit(1)

# Note: SSL verification is disabled for the HTTP client.
http_client = httpx.Client(verify=False)

# auth_header_name = "api-key"
auth_header_name = "Ocp-Apim-Subscription-Key"
print(f"Using authentication header: {auth_header_name}")

# Create the Azure OpenAI client with SSL verification disabled
client = AzureOpenAI(
    api_key=api_key,
    azure_endpoint=endpoint,
    api_version="2024-02-15-preview",
    http_client=http_client,
    default_headers={
        auth_header_name: api_key
    }
)

# Prepare and send the message
user_message = "Hello! Tell me a brief fun fact about cloud computing."
print(f"\nSending message to AI: \"{user_message}\"")

# Deployment name is required with Azure OpenAI
deployment_name = "gpt-4o-mini"  # Ensure this matches your actual deployment name
response = client.chat.completions.create(
    model=deployment_name,
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": user_message}
    ]
)

response_text = response.choices[0].message.content
if response_text:
    print("\nAI response:")
    print(response_text)
else:
    print("\nFailed to get a response from the AI service.")

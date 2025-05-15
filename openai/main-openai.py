import os
import sys
import httpx
from dotenv import load_dotenv
import openai
import time
import logging

load_dotenv()

# base_url should be in format:
# https://apim.contoso.com/openai/deployments/{deployment-id}
# E.g.,
# https://apim.contoso.com/openai/deployments/aoai
# The SDK will append /chat/completions automatically
base_url = os.getenv("BASE_URL")
api_key = os.getenv("API_KEY")

if not api_key or not base_url:
    print("Error: Azure OpenAI configuration is incomplete")
    print("Please set API_KEY and BASE_URL in the .env file")
    sys.exit(1)

model_deployment = "gpt-4o-mini"  # This should match your deployment name

# Important: Print the exact URL structure that will be used
print(f"Request will be sent to: {base_url}/chat/completions")
print(f"Using model deployment: {model_deployment}")

# Create a custom HTTP client with SSL verification disabled
# Disable SSL verification for testing purposes only!
http_client = httpx.Client(verify=False)

# auth_header_name = "api-key"
auth_header_name = "Ocp-Apim-Subscription-Key"

client = openai.OpenAI(
    api_key=api_key,
    base_url=base_url,
    default_headers={
        auth_header_name: api_key
    },
    # Set the custom HTTP client
    # Note: This is a workaround for SSL verification issues
    http_client=http_client
)

# Prepare and send the message
user_message = "Hello! Tell me a brief fun fact about cloud computing."
print(f"\nSending message to AI: \"{user_message}\"")

# Get and display the response
model_param = model_deployment

print("Sending request...")
start_time = time.time()

try:
    response = client.chat.completions.create(
        model=model_param,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_message}
        ]
    )
    
    elapsed_time = time.time() - start_time
    print(f"Request completed in {elapsed_time:.2f} seconds")
    
    response_text = response.choices[0].message.content
    if response_text:
        print("\nAI response:")
        print(response_text)
    else:
        print("\nFailed to get a response from the AI service.")

except Exception as e:
    print(f"Error during API call: {str(e)}")
    print(f"Error type: {type(e).__name__}")
    
    # Additional debugging info for the exception
    print("\nDetailed error information:")
    if hasattr(e, 'response') and e.response is not None:
        print(f"Response status code: {e.response.status_code}")
        print(f"Response headers: {e.response.headers}")
        print(f"Response body: {e.response.text}")
    sys.exit(1)

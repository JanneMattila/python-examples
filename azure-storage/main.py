# https://learn.microsoft.com/en-us/rest/api/storageservices/understanding-block-blobs--append-blobs--and-page-blobs#about-block-blobs
# https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/storage/azure-storage-blob
# https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/identity/azure-identity

# pip install azure-identity
# -> Successfully installed azure-identity-1.12.0
# pip install azure-storage-blob
# -> Successfully installed azure-storage-blob-12.15.0

# $env:storage_name="<your_storage_account_name>"
# $env:container_name="<your_storage_container_name>"
# $env:file_name="<your_filename>"

from azure.storage.blob import BlobServiceClient
from azure.identity import DefaultAzureCredential
import os

storage_name = os.environ["storage_name"]
container_name = os.environ["container_name"]
file_name = os.environ["file_name"]

token_credential = DefaultAzureCredential()

blob_service_client = BlobServiceClient(
    account_url="https://" + storage_name + ".blob.core.windows.net",
    credential=token_credential
)

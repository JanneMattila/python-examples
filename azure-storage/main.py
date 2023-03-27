# https://learn.microsoft.com/en-us/rest/api/storageservices/understanding-block-blobs--append-blobs--and-page-blobs#about-block-blobs

# https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/storage/azure-storage-blob
# https://azuresdkdocs.blob.core.windows.net/$web/python/azure-storage-blob/12.15.0/azure.storage.blob.html#azure.storage.blob.BlobClient

# https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/identity/azure-identity

# pip install azure-identity
# -> Successfully installed azure-identity-1.12.0
# pip install azure-storage-blob
# -> Successfully installed azure-storage-blob-12.15.0

# $env:storage_name="<your_storage_account_name>"
# $env:container_name="<your_storage_container_name>"
# $env:file_path="<your_file_path>"
# $env:file_name="<your_filename>"

# To generate demo file in bash:
# truncate -s 500m demo.bin

from azure.storage.blob import BlobServiceClient, BlobClient, BlobBlock
from azure.identity import DefaultAzureCredential
import os
import uuid

storage_name = os.environ["storage_name"]
container_name = os.environ["container_name"]
file_path = os.environ["file_path"]
file_name = os.environ["file_name"]

file_stats = os.stat(file_path + file_name)
print(f"File in MBs: {file_stats.st_size / (1024 * 1024)}")

token_credential = DefaultAzureCredential()

blob_service_client = BlobServiceClient(
    account_url=f"https://{storage_name}.blob.core.windows.net",
    credential=token_credential
)

container_client = blob_service_client.get_container_client(container_name)

# https://azuresdkdocs.blob.core.windows.net/$web/python/azure-storage-blob/12.15.0/azure.storage.blob.html#azure.storage.blob.BlobClient
max_block_size = 4000*1024*1024  # 4000 MB
max_single_put_size = 256*1024*1024  # 256 MB
min_large_block_upload_threshold = 256*1024*1024 + 1  # 256 MB
max_single_get_size = 256*1024*1024  # 256 MB
max_chunk_get_size = 256*1024*1024  # 256 MB
use_byte_buffer = False

# blob_client = container_client.get_blob_client(...)

blob_client = BlobClient(
    account_url=f"https://{storage_name}.blob.core.windows.net",
    container_name=container_name,
    credential=token_credential,
    blob_name=file_name, max_block_size=max_block_size, max_single_put_size=max_single_put_size,
    min_large_block_upload_threshold=min_large_block_upload_threshold, max_single_get_size=max_single_get_size,
    max_chunk_get_size=max_chunk_get_size, use_byte_buffer=use_byte_buffer
)

file_chunk_size = 256*1024*1024  # 256 MB
chunk_index = 1
block_list = []

with open(file_path + file_name, "rb") as data:
    while chunk := data.read(file_chunk_size):
        print(f"Chunk {chunk_index}")
        block_id = str(uuid.uuid4())
        blob_client.stage_block(
            block_id=block_id, data=chunk)
        block_list.append(BlobBlock(block_id=block_id))
        chunk_index += 1

blob_client.commit_block_list(block_list)


# Examples from
# https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/storage/azure-storage-blob/samples/blob_samples_hello_world.py
with open(file_path + file_name, "rb") as data:
    blob_client.upload_blob(data, blob_type="BlockBlob")

blob_client.delete_blob()

# https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/storage/azure-storage-blob/samples/blob_samples_hello_world.py#LL115-L128C66

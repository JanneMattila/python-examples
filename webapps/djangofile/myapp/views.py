from django.http import HttpResponse, StreamingHttpResponse
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
import os

def index(request):
    return HttpResponse("Hello there!")

def get_blob(request):
    container_name = request.GET.get('container')
    blob_path = request.GET.get('path')

    if not container_name or not blob_path:
        return HttpResponse("Missing 'container' or 'path' parameter", status=400)

    try:
        # Use managed identity to authenticate
        credential = DefaultAzureCredential()
        storage_account_name = os.getenv('AZURE_STORAGE_ACCOUNT_NAME')
        if not storage_account_name:
            return HttpResponse("Storage account name not set in environment variables", status=500)
        
        blob_service_client = BlobServiceClient(account_url=f"https://{storage_account_name}.blob.core.windows.net", credential=credential)
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_path)

        stream = blob_client.download_blob().chunks()
        response = StreamingHttpResponse(stream, content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(blob_path)}"'
        return response
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", status=500)
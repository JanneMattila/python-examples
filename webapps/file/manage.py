# Install the required packages:
# pip install django azure-identity azure-storage-blob
#
# Set required environment variables:
# cmd:
# set AZURE_STORAGE_ACCOUNT_NAME=your_storage_account_name
# powershell:
# $env:AZURE_STORAGE_ACCOUNT_NAME="your_storage_account_name"
#
# Run:
# python main.py runserver
#
# Open your web browser:
# http://localhost:8000

import os
import sys
from django.conf import settings
from django.http import HttpResponse, StreamingHttpResponse
from django.urls import path
from django.core.management import execute_from_command_line
from django.core.wsgi import get_wsgi_application
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient

# Step 2: Configure Django settings
settings.configure(
    DEBUG=True,
    ROOT_URLCONF=__name__,
    SECRET_KEY='a_random_secret_key',
    ALLOWED_HOSTS=['*'],
    MIDDLEWARE=[
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
    ],
)

# Step 3: Define a simple view
def index(request):
    return HttpResponse("Hello there!")

# Step 3: Define a view for the /api/blob endpoint
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

        # Stream the blob content
        stream = blob_client.download_blob().chunks()

        response = StreamingHttpResponse(stream, content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(blob_path)}"'
        return response
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", status=500)

# Step 4: Set up URL routing
urlpatterns = [
    path('', index),
    path('api/blob', get_blob),
]

# Step 5: Create a WSGI application
application = get_wsgi_application()

# Step 6: Run the Django development server
if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', __name__)
    execute_from_command_line(sys.argv)
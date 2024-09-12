# Django App Deployment to Azure App Service

This guide explains how to deploy a Django application to Azure App Service using Azure CLI.

[Configuring Gunicorn worker classes and other general settings](https://azureossd.github.io/2023/01/27/Configuring-Gunicorn-worker-classes-and-other-general-settings/)

[Oryx - Run](https://github.com/microsoft/Oryx/blob/main/doc/runtimes/python.md#run)

[Oryx - Configuration](https://github.com/microsoft/Oryx/blob/main/doc/configuration.md)

-> `PYTHON_ENABLE_GUNICORN_MULTIWORKERS`, `PYTHON_GUNICORN_CUSTOM_WORKER_NUM`, `PYTHON_GUNICORN_CUSTOM_THREAD_NUM`

[Handling concurrent requests with Python on Azure App Service Linux using Gunicorn and Flask](https://techcommunity.microsoft.com/t5/apps-on-azure-blog/handling-concurrent-requests-with-python-on-azure-app-service/ba-p/3913844)

```bash
# Create a virtual environment and install dependencies
py -m venv .venv

# Activate the virtual environment
.venv\scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the Django application
# python manage.py collectstatic # <- This is executed in App Service startup
python manage.py runserver

# You can test download e.g., 
# http://127.0.0.1:8000/api/blob?container=demo1&path=upload/500MB.bin

# Log in to your Azure account
az login

# Create a resource group
az group create --name "rg-app-services" --location swedencentral

# Create an App Service plan
az appservice plan create --name "asp" --resource-group "rg-app-services" --sku B1 --location swedencentral --is-linux

# Deploy your code to the web app
az webapp up --resource-group "rg-app-services" --plan "asp" --name "pythonfileapp00001" --launch-browser --runtime "PYTHON:3.12" --location swedencentral --sku B1

# Assign a managed identity to the web app
az webapp identity assign --resource-group "rg-app-services" --name "pythonfileapp00001" --identities "[system]"

# Configure environment variables
az webapp config appsettings set --resource-group "rg-app-services" --name "pythonfileapp00001" --settings AZURE_STORAGE_ACCOUNT_NAME=your_storage_account_name

az webapp config appsettings set --resource-group "rg-app-services" --name "pythonfileapp00001" --settings PYTHON_ENABLE_GUNICORN_MULTIWORKERS=true

# Alternatively, you can define these parameters as well:
az webapp config appsettings set --resource-group "rg-app-services" --name "pythonfileapp00001" --settings PYTHON_GUNICORN_CUSTOM_WORKER_NUM=4 # Default is  (2 * numCores) + 1
az webapp config appsettings set --resource-group "rg-app-services" --name "pythonfileapp00001" --settings PYTHON_GUNICORN_CUSTOM_THREAD_NUM=4 # Default is 1
```

Now you should be able to download multiple files concurrently:

![Django App and two downloads](./images/two-downloads.png)

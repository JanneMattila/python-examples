# myapp/urls.py

from django.urls import path
from .views import index, get_blob

urlpatterns = [
    path('', index),
    path('api/blob', get_blob),
]
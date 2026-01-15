"""
URL configuration for the Knowledge Assistant API project.

EXPLANATION:
This file is the specific entry point for routing incoming HTTP requests.
It defines the top-level URL patterns for the project.
- It maps the 'admin/' route to Django's built-in admin interface.
- It includes the 'assistant.urls' module for all requests starting with 'api/'.
  (e.g., http://localhost:8000/api/ask-question/ -> handled by assistant/urls.py)

Think of this as the "Main Switchboard" that directs traffic to the correct app.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('assistant.urls')),
]

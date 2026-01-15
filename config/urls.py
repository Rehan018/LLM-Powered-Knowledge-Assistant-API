"""
URL configuration for the Knowledge Assistant API project.

This file acts as the main switchboard for our web requests. When a user (or API client) 
hits our server, this file decides where that request should go.

I have set up two main paths:
- The 'admin/' path which takes you to the built-in Django admin panel.
- The 'api/' path which routes everything to our assistant app's URLs.

So if someone calls /api/ask-question/, this file passes it along to the assistant app to handle.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('assistant.urls')),
]

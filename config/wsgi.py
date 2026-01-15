"""
WSGI config for the Knowledge Assistant API project.

WSGI stands for Web Server Gateway Interface. It is basically the standard way for 
web servers to talk to Python web applications.

This file handles the synchronous requests (one by one) and is the entry point 
when we run the server or deploy it in a standard production environment.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()

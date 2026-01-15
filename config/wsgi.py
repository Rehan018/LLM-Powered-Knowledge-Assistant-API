"""
WSGI config for the Knowledge Assistant API project.

EXPLANATION:
WSGI (Web Server Gateway Interface) is the standard synchronous interface between 
web servers and Python web applications.

Roles of this file:
1.  **Entry Point**: It is the entry point for WSGI-compatible web servers (like Gunicorn/uWSGI).
2.  **Synchronous Handling**: It handles requests one by one (blocking).
3.  **Deployment**: In production, the web server points to this `application` callable to start the site.

For this project, it's used when running `runserver` or deploying in a standard synchronous environment.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()

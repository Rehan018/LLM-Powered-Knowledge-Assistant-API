"""
ASGI config for the Knowledge Assistant API project.

ASGI stands for Asynchronous Server Gateway Interface. It is the modern sibling of WSGI 
that allows us to handle multiple requests at the same time (asynchronously).

Although our simple API is mostly synchronous right now, having this file ready means 
we can easily add real-time features like WebSockets in the future without changing the architecture.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_asgi_application()

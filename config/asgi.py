"""
ASGI config for the Knowledge Assistant API project.

EXPLANATION:
ASGI (Asynchronous Server Gateway Interface) is the spiritual successor to WSGI, 
designed to handle asynchronous workloads.

Roles of this file:
1.  **Async Entry Point**: Allows the application to handle concurrent requests (non-blocking).
2.  **Modern Features**: Required for WebSockets, HTTP/2, and long-polling (though not strictly used in this simple API).
3.  **Performance**: Enables higher concurrency if deployed with an ASGI server like Uvicorn or Daphne.

While our current Views are synchronous, having ASGI config ready ensures the project is future-proof for async features.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_asgi_application()

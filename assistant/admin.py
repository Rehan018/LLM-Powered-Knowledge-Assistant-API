"""
Django Admin Configuration.

EXPLANATION:
This file is used to register models with the Django Admin interface.
The Admin interface is a built-in, ready-to-use user interface for database management.

To expose the models `KnowledgeDocument` and `InteractionLog` to the admin:
1.  Import the models: `from .models import KnowledgeDocument, InteractionLog`
2.  Register them: `admin.site.register(KnowledgeDocument)`

This allows you to see uploaded files and user-bot interactions via the web UI.
"""

from django.contrib import admin

# Register your models here.

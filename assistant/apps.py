"""
App Configuration.

EXPLANATION:
This file defines the configuration for the 'assistant' application.
It tells Django:
1.  The name of the app ('assistant').
2.  The default type for primary keys (BigAutoFiled).

It is referenced in `config/settings.py` under `INSTALLED_APPS` as 'assistant.apps.AssistantConfig'.
"""

from django.apps import AppConfig


class AssistantConfig(AppConfig):
    name = 'assistant'

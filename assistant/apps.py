"""
App Configuration.

This is a standard Django configuration file. It simple defines the name of our application 
('assistant') and sets the default field type for auto-incrementing IDs. 
Django uses this to identify and load our app correctly.
"""

from django.apps import AppConfig


class AssistantConfig(AppConfig):
    name = 'assistant'

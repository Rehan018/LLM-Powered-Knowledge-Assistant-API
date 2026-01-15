"""
URL Routing for the Assistant Application.

This file handles the specific URL patterns for our 'assistant' app. 
It maps the specific 'ask-question/' path to the view we just verified.

When this is hooked up to the main project URLs, the full endpoint becomes 
'api/ask-question/'. This is where we will send our POST requests.
"""

from django.urls import path
from .views import AskQuestionView

urlpatterns = [
    path('ask-question/', AskQuestionView.as_view(), name='ask-question'),
]

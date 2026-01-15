"""
URL Routing for the Assistant Application.

EXPLANATION:
This file defines the specific URL patterns belonging to the `assistant` app.
It determines which View handles a specific URL path.

Routes:
- **'ask-question/'**: Maps to `AskQuestionView`.

When included in the main `config/urls.py` with prefix `api/`, the final URL becomes:
`POST http://localhost:8000/api/ask-question/`
"""

from django.urls import path
from .views import AskQuestionView

urlpatterns = [
    path('ask-question/', AskQuestionView.as_view(), name='ask-question'),
]

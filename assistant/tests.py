"""
Unit Tests for the Assistant App.

EXPLANATION:
This file is where we write automated tests to ensure our code works as expected.

What should be tested here?
1.  **Models**: Verify that `KnowledgeDocument` creates correctly.
2.  **Services**: Test `IngestionService` (does it chunk text?) and `RAGService` (does it return chunks?).
3.  **Views**: Test the API endpoint `POST /api/ask-question/` for 200 OK and valid JSON response.

Running tests:
`python manage.py test`
"""

from django.test import TestCase

# Create your tests here.

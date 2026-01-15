"""
Management Command for Knowledge Base Ingestion.

EXPLANATION:
This file exposes our `IngestionService` to the command line interface (CLI).
It allows admins/developers to trigger the ingestion process by running:
`python manage.py ingest_kb`

Why is this a separate command?
- Ingestion is heavy (parsing PDFs, generating embeddings).
- It shouldn't happen during a web request (which would time out).
- It's a maintenance task run whenever new documents are added.
"""

from django.core.management.base import BaseCommand
from assistant.services.ingestion import IngestionService

class Command(BaseCommand):
    help = 'Ingests the PDF knowledge base into FAISS vector store'

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting Knowledge Base Ingestion...")
        service = IngestionService()
        result = service.process_knowledge_base()
        self.stdout.write(self.style.SUCCESS(result))

"""
Management Command for Knowledge Base Ingestion.

This file allows me to run the ingestion process directly from the terminal using:
'python manage.py ingest_kb'

I made this a separate command because processing PDFs and generating embeddings 
is a heavy task. We don't want to do this while a user is waiting for a web page to load. 
It's meant to be run as a background task or maintenance script.
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

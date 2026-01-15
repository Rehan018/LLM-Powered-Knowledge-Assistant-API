from django.core.management.base import BaseCommand
from assistant.services.ingestion import IngestionService

class Command(BaseCommand):
    help = 'Ingests the PDF knowledge base into FAISS vector store'

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting Knowledge Base Ingestion...")
        service = IngestionService()
        result = service.process_knowledge_base()
        self.stdout.write(self.style.SUCCESS(result))

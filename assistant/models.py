"""
Database Models for the Knowledge Assistant Application.

EXPLANATION:
This file defines the data structure for our application using Django's ORM.

1. **KnowledgeDocument**:
   - Represents a PDF file that has been uploaded and processed.
   - Tracks the file name, path, upload time, and processing status.
   - Useful for managing the Knowledge Base and ensuring files aren't re-processed unnecessarily.

2. **InteractionLog**:
   - Acts as an audit trail for the system.
   - Records every User Question, the generated AI Answer, and the Source Citations.
   - Enabling this allows for future analytics (e.g., "What are users asking most?").
"""

from django.db import models

class KnowledgeDocument(models.Model):
    file_name = models.CharField(max_length=255)
    file_path = models.TextField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_processed = models.BooleanField(default=False)

    def __str__(self):
        return self.file_name

class InteractionLog(models.Model):
    question = models.TextField()
    answer = models.TextField()
    sources = models.JSONField(default=list)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Q: {self.question[:50]}..."

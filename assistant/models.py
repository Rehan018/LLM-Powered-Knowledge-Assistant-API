"""
Database Models for the Knowledge Assistant Application.

Here I have defined the data structures (models) for our application. 

I've created two main models:
1. KnowledgeDocument: This tracks all the PDF files we've uploaded. It keeps a record of the filename, path, and whether we've finished processing it. This helps us avoid re-processing the same file twice.

2. InteractionLog: This is like our system's diary. It records every question a user asks, the answer our AI gives, and the specific sources it used. This is great for looking back at what users are interested in.
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

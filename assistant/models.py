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

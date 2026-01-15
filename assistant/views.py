"""
API Main Logic (Views) for the Knowledge Assistant.

EXPLANATION:
This file contains the API endpoints exposed to the user. It bridges the HTTP requests
with the business logic (RAG Service).

**AskQuestionView (POST /api/ask-question/)**:
1.  **Input**: Receives a JSON payload `{"question": "..."}`.
2.  **Validation**: Checks if the question is provided.
3.  **Processing**: Calls `RAGService().handle_query(question)` to get the answer.
4.  **Error Handling**: Catches errors (e.g., missing index files, LLM failures) and returns appropriate HTTP status codes.
5.  **Output**: Returns a JSON response `{"answer": "...", "sources": [...]}`.

This view keeps the "Controller" logic thin by delegating heavy lifting to the Service layer (`rag_service.py`).
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services.rag_service import RAGService

class AskQuestionView(APIView):
    def post(self, request):
        question = request.data.get('question')
        if not question:
            return Response({"error": "Question is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            rag_service = RAGService()
            answer, sources = rag_service.handle_query(question)
            return Response({
                "answer": answer,
                "sources": sources
            }, status=status.HTTP_200_OK)
        except FileNotFoundError as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"error": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

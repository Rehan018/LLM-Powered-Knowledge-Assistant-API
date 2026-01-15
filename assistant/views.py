"""
API Main Logic (Views) for the Knowledge Assistant.

This file contains the API endpoints that users actually interact with. It acts as a bridge 
between the incoming request and our business logic.

The main view here is 'AskQuestionView'. When a user sends a question:
1. It validates that the question actually exists.
2. It passes the question to our RAG Service (the brain of the operation) to get an answer.
3. If everything goes well, it returns the answer and sources as a neat JSON response.
4. If something goes wrong (like a missing file), it handles the error gracefully.

I've kept this file simple intentionally - it delegates the heavy lifting to the service layer.
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

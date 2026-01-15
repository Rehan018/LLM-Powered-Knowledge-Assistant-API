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

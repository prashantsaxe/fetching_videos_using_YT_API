from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.routers import DefaultRouter
from .services import fetch_latest_videos

class YoutubeVideoViewSet(viewsets.ViewSet):

    
    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get('q', '')
        max_results = request.query_params.get('max_results', 10)
        
        try:
            max_results = int(max_results)
        except ValueError:
            max_results = 10
            
        if not query:
            return Response(
                {"error": "Search query is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        try:
            videos = fetch_latest_videos(query=query, max_results=max_results)
            return Response(videos)
        except Exception as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# Create a router and register our viewset
router = DefaultRouter()
router.register(r'videos', YoutubeVideoViewSet, basename='videos')
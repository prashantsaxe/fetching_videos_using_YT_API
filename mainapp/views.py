from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from .models import Video
from .serializers import VideoSerializer
from .tasks import fetch_youtube_videos

class VideoViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for viewing YouTube videos.
    """
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    
    @method_decorator(cache_page(60))  # Cache for 60 seconds
    def list(self, request, *args, **kwargs):
        """Get all videos with pagination"""
        return super().list(request, *args, **kwargs)
    
    @action(detail=False, methods=['get'])
    @method_decorator(cache_page(300))  # Cache for 5 minutes
    def by_channel(self, request):
        """Get videos grouped by channel"""
        channel = request.query_params.get('channel', None)
        
        if channel:
            videos = Video.objects.filter(channel_title__icontains=channel)
        else:
            videos = Video.objects.all()
            
        page = self.paginate_queryset(videos)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
            
        serializer = self.get_serializer(videos, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def fetch_videos(self, request):
        """Trigger asynchronous fetching of videos"""
        query = request.data.get('query', 'cricket')
        max_results = request.data.get('max_results', 10)
        
        try:
            task = fetch_youtube_videos.delay(query, max_results)
            
            return Response({
                'status': 'Task scheduled',
                'task_id': task.id,
                'message': f"Started fetching videos for '{query}' with max results {max_results}"
            })
        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
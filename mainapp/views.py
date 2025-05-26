from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from .models import Video
from .serializers import VideoSerializer

class VideoViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for viewing YouTube videos.
    
    list:
        Returns a paginated list of videos sorted by published_at in descending order.
    retrieve:
        Returns details of a specific video.
    """
    queryset = Video.objects.all().order_by('-published_at')
    serializer_class = VideoSerializer
    
    def list(self, request, *args, **kwargs):
        """
        Get all videos with pagination, sorted by published date (newest first).
        """
        # The queryset is already ordered by -published_at in the class definition
        # Just return the standard list implementation which includes pagination
        return super().list(request, *args, **kwargs)
    
    @action(detail=False, methods=['get'])
    def by_channel(self, request):
        """Get videos grouped by channel"""
        channel = request.query_params.get('channel', None)
        
        if channel:
            videos = Video.objects.filter(channel_title__icontains=channel).order_by('-published_at')
        else:
            videos = Video.objects.all().order_by('-published_at')
            
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
            from .tasks import fetch_youtube_videos
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
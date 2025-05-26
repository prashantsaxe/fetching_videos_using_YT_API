from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from .models import Video
from .serializers import VideoSerializer
from .services import fetch_latest_videos

class VideoPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class VideoListView(generics.ListAPIView):
    queryset = Video.objects.all().order_by('-published_at')
    serializer_class = VideoSerializer
    pagination_class = VideoPagination

    def get_queryset(self):
        query = self.request.query_params.get('query', None)
        if query:
            return self.queryset.filter(title__icontains=query)
        return self.queryset

class VideoFetchView(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        fetch_latest_videos()
        return Response({"message": "Fetching latest videos initiated."}, status=202)
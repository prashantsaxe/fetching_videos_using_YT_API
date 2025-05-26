from rest_framework import serializers
from .models import Video

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'video_id', 'title', 'description', 'published_at', 
                  'thumbnail_url', 'channel_title', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
from celery import shared_task
import requests
from .models import Video

@shared_task
def fetch_latest_videos(search_query='cricket'):
    api_key = 'AIzaSyANOIK8E6JYFiNzde_qgUlLwPyKu9dHAoQ'
    url = f'https://www.googleapis.com/youtube/v3/search?part=snippet&q={search_query}&order=date&maxResults=10&key={api_key}'
    
    response = requests.get(url)
    data = response.json()
    
    for item in data.get('items', []):
        video_id = item['id'].get('videoId')
        if video_id:
            Video.objects.update_or_create(
                video_id=video_id,
                defaults={
                    'title': item['snippet']['title'],
                    'description': item['snippet']['description'],
                    'published_at': item['snippet']['publishedAt'],
                    'thumbnail_url': item['snippet']['thumbnails']['default']['url'],
                }
            )
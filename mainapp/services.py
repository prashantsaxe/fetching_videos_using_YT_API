from django.conf import settings
import requests

YOUTUBE_API_URL = "https://www.googleapis.com/youtube/v3/search"

def fetch_latest_videos(query, max_results=10):
    params = {
        'part': 'snippet',
        'q': query,
        'type': 'video',
        'order': 'date',
        'maxResults': max_results,
        'key': settings.YOUTUBE_API_KEY
    }
    
    response = requests.get(YOUTUBE_API_URL, params=params)
    
    if response.status_code == 200:
        return response.json().get('items', [])
    else:
        response.raise_for_status()
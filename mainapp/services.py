from django.conf import settings
import requests
from datetime import datetime
from .models import Video
import pytz

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

def fetch_and_save_cricket_videos():
    """Fetch cricket videos from YouTube and save them to the database"""
    try:
        videos = fetch_latest_videos(query="cricket", max_results=10)
        
        for video_data in videos:
            video_id = video_data['id']['videoId']
            snippet = video_data['snippet']
            
            # Parse the published date
            published_at = datetime.strptime(
                snippet['publishedAt'], 
                '%Y-%m-%dT%H:%M:%SZ'
            ).replace(tzinfo=pytz.UTC)
            
            # Create or update the video in the database
            Video.objects.update_or_create(
                video_id=video_id,
                defaults={
                    'title': snippet['title'],
                    'description': snippet['description'],
                    'published_at': published_at,
                    'thumbnail': snippet['thumbnails']['high']['url'],
                    'channel_title': snippet['channelTitle']
                }
            )
        
        return f"Successfully fetched and saved {len(videos)} cricket videos"
    except Exception as e:
        return f"Error fetching videos: {str(e)}"
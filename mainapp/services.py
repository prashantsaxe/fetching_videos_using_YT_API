from django.conf import settings
import aiohttp
import asyncio
from datetime import datetime
from asgiref.sync import sync_to_async
from .models import Video
import logging

logger = logging.getLogger(__name__)

YOUTUBE_API_URL = "https://www.googleapis.com/youtube/v3/search"

async def async_fetch_videos(query, max_results=10):
    """Asynchronously fetch videos from YouTube API"""
    params = {
        'part': 'snippet',
        'q': query,
        'type': 'video',
        'order': 'date',
        'maxResults': max_results,
        'key': settings.YOUTUBE_API_KEY
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.get(YOUTUBE_API_URL, params=params) as response:
            if response.status == 200:
                data = await response.json()
                return data.get('items', [])
            else:
                text = await response.text()
                logger.error(f"YouTube API error: {response.status} - {text}")
                response.raise_for_status()

@sync_to_async
def save_video_to_db(video_data):
    """Save a single video to the database"""
    try:
        video_id = video_data['id']['videoId']
        snippet = video_data['snippet']
        
        # Parse the published date
        published_at = datetime.strptime(
            snippet['publishedAt'], 
            '%Y-%m-%dT%H:%M:%SZ'
        )
        
        # Create or update the video in the database
        video, created = Video.objects.update_or_create(
            video_id=video_id,
            defaults={
                'title': snippet['title'],
                'description': snippet['description'],
                'published_at': published_at,
                'thumbnail': snippet['thumbnails']['high']['url'],
                'channel_title': snippet['channelTitle']
            }
        )
        
        return video, created
    except Exception as e:
        logger.error(f"Error saving video {video_data.get('id', {}).get('videoId', 'unknown')}: {str(e)}")
        return None, False

async def async_fetch_and_save_videos(query="cricket", max_results=10):
    """Fetch videos and save them to the database asynchronously"""
    try:
        videos = await async_fetch_videos(query, max_results)
        
        # Process videos concurrently
        tasks = [save_video_to_db(video) for video in videos]
        results = await asyncio.gather(*tasks)
        
        saved_count = sum(1 for video, created in results if video is not None)
        new_count = sum(1 for _, created in results if created)
        
        return {
            'success': True,
            'message': f"Successfully processed {len(videos)} videos. Saved {saved_count} ({new_count} new)."
        }
    except Exception as e:
        logger.error(f"Error in async_fetch_and_save_videos: {str(e)}")
        return {
            'success': False,
            'message': f"Error: {str(e)}"
        }

def fetch_latest_videos(query, max_results=10):
    """Synchronous version for backward compatibility"""
    import requests
    
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


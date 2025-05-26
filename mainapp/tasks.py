import logging
import requests
from datetime import datetime
from django.conf import settings
from celery import shared_task
from dateutil import parser
from .models import Video

logger = logging.getLogger(__name__)

@shared_task
def fetch_youtube_videos(query='cricket', max_results=10):
    """
    Fetch YouTube videos based on query and save to database.
    
    Args:
        query (str): Search term for YouTube API
        max_results (int): Maximum number of results to return
    
    Returns:
        dict: Summary of the operation
    """
    logger.info(f"Fetching YouTube videos for query: '{query}', max results: {max_results}")
    
    api_key = settings.YOUTUBE_API_KEY
    api_url = "https://www.googleapis.com/youtube/v3/search"
    
    params = {
        'part': 'snippet',
        'q': query,
        'type': 'video',
        'order': 'date',
        'maxResults': max_results,
        'key': api_key
    }
    
    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()  # Raise exception for 4XX/5XX responses
        
        data = response.json()
        items = data.get('items', [])
        
        new_videos = 0
        updated_videos = 0
        
        for item in items:
            video_id = item['id']['videoId']
            snippet = item['snippet']
            
            # Parse the published date
            published_at = parser.parse(snippet['publishedAt'])
            
            # Get thumbnail URL (use high quality if available, else default)
            thumbnails = snippet.get('thumbnails', {})
            thumbnail_url = thumbnails.get('high', {}).get('url') or thumbnails.get('default', {}).get('url', '')
            
            # Create or update video in database
            video, created = Video.objects.update_or_create(
                video_id=video_id,
                defaults={
                    'title': snippet.get('title', ''),
                    'description': snippet.get('description', ''),
                    'published_at': published_at,
                    'thumbnail_url': thumbnail_url,
                    'channel_title': snippet.get('channelTitle', '')
                }
            )
            
            if created:
                new_videos += 1
            else:
                updated_videos += 1
        
        result = {
            'success': True,
            'query': query,
            'total_fetched': len(items),
            'new_videos': new_videos,
            'updated_videos': updated_videos
        }
        logger.info(f"YouTube API fetch successful: {result}")
        return result
        
    except requests.exceptions.RequestException as e:
        error_msg = f"YouTube API request failed: {str(e)}"
        logger.error(error_msg)
        return {
            'success': False,
            'query': query,
            'error': error_msg
        }
    except Exception as e:
        error_msg = f"Error processing YouTube videos: {str(e)}"
        logger.error(error_msg)
        return {
            'success': False,
            'query': query,
            'error': error_msg
        }

@shared_task
def clean_old_videos(days=30):
    """Delete videos older than specified days"""
    from django.utils import timezone
    import datetime
    
    cutoff_date = timezone.now() - datetime.timedelta(days=days)
    
    deleted, _ = Video.objects.filter(published_at__lt=cutoff_date).delete()
    
    logger.info(f"Cleaned up {deleted} videos older than {days} days")
    return {'deleted_count': deleted}
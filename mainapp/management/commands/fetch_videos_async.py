from django.core.management.base import BaseCommand
import asyncio
from asgiref.sync import async_to_sync
from mainapp.services import async_fetch_and_save_videos

class Command(BaseCommand):
    help = 'Asynchronously fetch latest videos from YouTube and save to database'

    def add_arguments(self, parser):
        parser.add_argument('--query', type=str, default='cricket', help='Search query')
        parser.add_argument('--max-results', type=int, default=10, help='Maximum number of results')

    def handle(self, *args, **options):
        query = options['query']
        max_results = options['max_results']
        
        self.stdout.write(f"Fetching videos for query: '{query}' (max: {max_results})")
        
        # Run the async function
        result = async_to_sync(async_fetch_and_save_videos)(query, max_results)
        
        if result['success']:
            self.stdout.write(self.style.SUCCESS(result['message']))
        else:
            self.stdout.write(self.style.ERROR(result['message']))
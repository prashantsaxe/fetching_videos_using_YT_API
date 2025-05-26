from django.contrib import admin
from .models import Video

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'channel_title', 'published_at', 'created_at')
    search_fields = ('title', 'description', 'channel_title')
    list_filter = ('channel_title', 'published_at')
    date_hierarchy = 'published_at'
    readonly_fields = ('created_at', 'updated_at')